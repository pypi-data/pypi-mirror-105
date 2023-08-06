"""


struct <name> field1 type1 ... fieldn typen

Layout:
  [ instance size ]: is not static
  static-field1
  ..
  static-fieldn
  [ offset field 2 ]
  [ offset ...
  [ offset field n ]
  [ dynamic-field1 ]
  [ ...
  [ dynamic-fieldn ]

Current implementation:
    1) instance stores the actual offsets for dynamic offset. Although it is wasteful for memory, it avoids a double round trip. This hinges on the structure being frozen at initializations.
    2) cache mechanism in place, but not used so far

Struct class:
- _size: class size, None if not static
- _fields: list of fields
- _d_fields: list of dynamic fields
- _s_fields: list of dynamic fields

Struct instance:
- _offsets: cached offsets of dynamic fields dict indexed by field.index
- _sizes: cached sizes of dynamic fields dict indexed by field.index
- _cache: cached python objects for __get__

Field instance:
- ftype
- index
- name
- offset
- is_static_type
- has_update
- readonly



"""
import logging
from typing import Callable


from .typeutils import (
    get_a_buffer,
    dispatch_arg,
    Info,
    _to_slot_size,
    _is_dynamic,
)

from .scalar import Int64
from .array import Array
from . import capi


log = logging.getLogger(__name__)


class Field:
    def __init__(
        self, ftype, default=None, readonly=False, default_factory=None
    ):
        self.ftype = ftype
        self.default = default
        self.default_factory = default_factory
        self.index = None  # filled by class creation
        self.name = None  # filled by class creation
        self.offset = None  # filled by class creation
        self.is_reference = None  # filled by class creation
        self.has_update = False  # filled by class creation
        self.readonly = readonly

    def __repr__(self):
        return f"<Field{self.index} {self.name} at {self.offset}>"

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        else:
            if self.index in instance._cache:
                return instance._cache[self.index]
            else:
                offset = instance._offset + self.get_offset(instance)
                return self.ftype._from_buffer(instance._buffer, offset)

    def __set__(self, instance, value):
        """
        A value can be:
          - python value: dict or scalar or list...
          - another instance of the same type
          - ???a buffer_protocol object???
        """
        if self.readonly:
            raise AttributeError(f"Field {self.name} is read-only")

        if hasattr(self.ftype, "_update"):
            self.__get__(instance)._update(value)
        else:  # TODO check if below is really needed
            offset = instance._offset + self.get_offset(instance)
            self.ftype._to_buffer(instance._buffer, offset, value)

    def get_offset(self, instance):  # compatible with info
        if self.is_reference:
            return instance._offsets[self.index]
        else:
            return self.offset

    def get_default(self):
        if self.default_factory is None:
            if self.default is None:
                return self.ftype()
            else:
                return dispatch_arg(self.ftype, self.default)
        else:
            return self.default_factory()

    def value_from_args(self, arg):
        if self.name in arg:
            return arg[self.name]
        else:
            return self.get_default()

    def _get_c_offset(self, conf):
        itype = conf.get("itype", "int64_t")
        if self.is_reference:
            doffset = f"offset+{self.offset}"  # starts of data
            return [f"  offset+= *(/*gpuglmem*/{itype}*)((/*gpuglmem*/char*) obj + {doffset});"]
        else:
            return self.offset


class MetaStruct(type):
    def __new__(cls, name, bases, data):
        offset = 0
        fields = []
        s_fields = []
        d_fields = []
        is_static = True
        findex = 0
        for aname, field in data.items():
            if hasattr(field, "_inspect_args"):
                data[aname] = Field(field)
        for aname, field in data.items():
            if isinstance(field, Field):
                field.index = findex
                findex += 1
                field.name = aname
                if hasattr(field.ftype, "_update"):
                    field.has_update = True
                fields.append(field)
                if field.ftype._size is None:
                    d_fields.append(field)
                    is_static = False
                else:
                    s_fields.append(field)
        data["_fields"] = fields
        data["_s_fields"] = s_fields
        data["_d_fields"] = d_fields

        if is_static:
            offset = 0
            for field in fields:
                field.offset = offset
                field.is_reference = False
                offset += _to_slot_size(field.ftype._size)
            size = offset

            def _get_size(self):
                return self.__class__._size

            def _inspect_args(cls, *args, **kwargs):
                return Info(size=cls._size, is_static_size=True)

        else:
            size = None
            for field in fields:
                offset = 8  # first slot is instance size
                for field in s_fields:
                    field.offset = offset
                    field.is_reference = False
                    offset += _to_slot_size(field.ftype._size)
                # other dynamic fields
                for field in d_fields[1:]:
                    field.offset = offset
                    field.is_reference = True
                    offset += _to_slot_size(8)
                # first dynamic field
                d_fields[0].offset = offset
                d_fields[0].is_reference = False

            def _get_size(self):
                return Int64._from_buffer(self._buffer, self._offset)

            def _inspect_args(cls, *args, **kwargs):
                log.debug(f"get size for {cls} from {args} {kwargs}")
                if len(args) == 1:
                    arg = args[0]
                    if isinstance(arg, dict):
                        arg = cls._pre_init(**arg)
                        offsets = {}  # offset of dynamic data
                        extra = {}
                        offset = d_fields[
                            0
                        ].offset  # offset first dynamic data
                        log.debug(f"{arg}")
                        for field in cls._d_fields:
                            farg = field.value_from_args(arg)
                            log.debug(
                                f"get size for field `{field.name}` using `{farg}`"
                            )
                            finfo = dispatch_arg(
                                field.ftype._inspect_args, farg
                            )
                            if hasattr(finfo, "_offsets"):  # is dinamic
                                extra[field.index] = finfo
                            offsets[field.index] = offset
                            offset += _to_slot_size(finfo.size)
                        # _offsets is used to because of field.get_offset(info)
                        info = Info(size=offset, _offsets=offsets)
                        if len(extra) > 0:
                            info.extra = extra
                        return Info(size=offset, _offsets=offsets, extra=extra)
                    elif isinstance(arg, cls):
                        size = arg._get_size()
                        return Info(size=size)
                    else:
                        raise ValueError(f"{arg} Not valid type for {cls}")
                else:  # python argument
                    return cls._inspect_args(kwargs)

        data["_size"] = size
        data["_get_size"] = _get_size
        data["_inspect_args"] = classmethod(_inspect_args)
        if "_c_type" not in data:
            data["_c_type"] = name

        return type.__new__(cls, name, bases, data)

    def __getitem__(cls, shape):
        return Array.mk_arrayclass(cls, shape)


class Struct(metaclass=MetaStruct):
    _fields: list
    _d_fields: list
    _inspect_args: Callable

    @classmethod
    def _pre_init(cls, *arg, **kwargs):
        return kwargs

    def _post_init(self):
        pass

    @classmethod
    def _from_buffer(cls, buffer, offset):
        self = object.__new__(cls)
        self._buffer = buffer
        self._offset = offset
        _offsets = {}
        for field in self._d_fields:
            offset = self._offset + field.offset
            val = Int64._from_buffer(self._buffer, offset)
            _offsets[field.index] = val
        self._offsets = _offsets
        self._cache = {}
        self._post_init()
        return self

    @classmethod
    def _to_buffer(cls, buffer, offset, value, info=None):
        if isinstance(value, cls):  # binary copy
            buffer.update_from_xbuffer(
                offset, value._buffer, value._offset, value._size
            )
        else:  # value must be a dict, again potential disctructive
            value = cls._pre_init(**value)
            if info is None:
                info = cls._inspect_args(value)
            if cls._size is None:
                Int64._to_buffer(buffer, offset, info.size)
            if hasattr(
                info, "_offsets"
            ):  # if it has a least two dynamic fields
                cls._set_offsets(buffer, offset, info._offsets)
            extra = getattr(info, "extra", {})
            for field in cls._fields:
                fvalue = field.value_from_args(value)
                foffset = offset + field.get_offset(info)
                finfo = extra.get(field.index)
                field.ftype._to_buffer(buffer, foffset, fvalue, finfo)

    def _update(self, value):
        # check if direct copy is possible
        if isinstance(value, self.__class__) and value._size == self._size:
            self._buffer.update_from_xbuffer(
                self._offset, value._buffer, value._offset, value._size
            )
        else:
            for field in self._fields:
                if field.name in value:
                    field.__set__(self, value[field.name])

    def __init__(self, _context=None, _buffer=None, _offset=None, **kwargs):
        """
        Create new struct in buffer from offset.
        If offset not provide
        """
        cls = self.__class__
        # compute resources
        info = cls._inspect_args(**kwargs)
        self._size = info.size
        # acquire buffer
        self._buffer, self._offset = get_a_buffer(
            info.size, _context, _buffer, _offset
        )
        # if dynamic struct store dynamic offsets
        if hasattr(info, "_offsets"):
            self._offsets = info._offsets  # struct offsets
        cls._to_buffer(self._buffer, self._offset, kwargs, info)
        self._cache = {}
        self._post_init()

    @classmethod
    def _set_offsets(cls, buffer, offset, loffsets):
        log.debug(f"{cls} set offset {loffsets}")
        for index, data_offset in loffsets.items():
            foffset = offset + cls._fields[index].offset
            Int64._to_buffer(buffer, foffset, data_offset)

    def _to_dict(self):
        return {field.name: field.__get__(self) for field in self._fields}

    def __iter__(self):
        for field in self._fields:
            yield field.name

    def __getitem__(self, key):
        for field in self._fields:
            if field.name == key:
                return field.__get__(self)
        raise KeyError("{key} not found")

    def __contains__(self, key):
        for field in self._fields:
            if field.name == key:
                return True
        else:
            return False

    def __repr__(self):
        fields = (
            (field.name, repr(getattr(self, field.name)))
            for field in self._fields
        )
        fields = ", ".join(f"{k}={v}" for k, v in fields)
        longform = f"{self.__class__.__name__}({fields})"
        if len(longform) > 60:
            return f"{self.__class__.__name__}(...)"
        else:
            return longform

    @classmethod
    def _gen_data_paths(cls, base=None):
        paths = []
        if base is None:
            base = []
        for field in cls._fields:
            path = base + [field]
            paths.append(path)
            if hasattr(field.ftype, "_gen_data_paths"):
                paths.extend(field.ftype._gen_data_paths(path))
        return paths

    @classmethod
    def _gen_c_api(cls, conf={}):
        specs_list = cls._gen_data_paths()
        return capi.gen_code(cls, specs_list, conf)
