# coding=utf-8
import abc
import csv
import dataclasses
import enum
import io
from typing import Callable, Generic, MutableSequence, Optional, Type, TypeVar, Union, cast, Iterable, Any

import jsons
from ruamel.yaml import YAML

try:
    import ujson as json
except ImportError:
    import json


T = TypeVar('T')
StateHolder = jsons.fork()


class Serializer(Generic[T]):
    @abc.abstractmethod
    def __call__(self, obj: T, **_) -> object:
        pass


class Deserializer(Generic[T]):
    @abc.abstractmethod
    def __call__(self, obj: object, cls: type, **_) -> T:
        pass


@dataclasses.dataclass(frozen=True)
class ClassSerializer(Serializer[T]):
    strip_nulls: bool = False
    strip_privates: bool = False
    strip_properties: bool = True
    strip_class_variables: bool = True
    strip_attr: Optional[Union[str, MutableSequence[str], tuple[str]]] = None
    key_transformer: Optional[Callable[[str], str]] = None
    verbose: Union[jsons.Verbosity, bool] = False
    strict: bool = True

    def __call__(self, obj: T, **kwargs) -> dict:
        return jsons.default_object_serializer(
            **{
                **kwargs,
                "obj": obj,
                "strip_nulls": self.strip_nulls,
                "strip_privates": self.strip_privates,
                "strip_properties": self.strip_properties,
                "strip_class_variables": self.strip_class_variables,
                "strip_attr": self.strip_attr,
                "key_transformer": self.key_transformer,
                "verbose": self.verbose,
                "strict": self.strict
            }
        )


@dataclasses.dataclass(frozen=True)
class ClassDeserializer(Deserializer[T]):
    key_transformer: Optional[Callable[[str], str]] = None
    strict: bool = True

    def __call__(self, obj: dict, cls: type, **kwargs) -> T:
        return jsons.default_object_deserializer(
            **{
                **kwargs,
                "obj": obj,
                "cls": cls,
                "key_transformer": self.key_transformer,
                "strict": self.strict
            }

        )


def _set_serializer(cls: T, serializer: ClassSerializer[T]) -> None:
    cls.__serializer__ = serializer


def _pop_serializer(cls: T) -> ClassSerializer:
    if hasattr(cls, "__serializer__"):
        serializer = cls.__serializer__
        del cls.__serializer__
    else:
        serializer = ClassSerializer()

    return serializer


def _set_deserializer(cls: T, deserializer: ClassDeserializer[T]) -> None:
    cls.__deserializer__ = deserializer


def _pop_deserializer(cls: T) -> ClassDeserializer:
    if hasattr(cls, "__deserializer__"):
        deserializer = cls.__deserializer__
        del cls.__deserializer__
    else:
        deserializer = ClassDeserializer()

    return deserializer


def with_serializer(serializer: ClassSerializer[T]) -> Callable[[T], T]:
    def class_wrapper(cls: T) -> T:
        _set_serializer(cls=cls, serializer=serializer)

        return cls

    return class_wrapper


def with_deserializer(deserializer: ClassDeserializer[T]) -> Callable[[T], T]:
    def class_wrapper(cls: T) -> T:
        _set_deserializer(cls=cls, deserializer=deserializer)

        return cls

    return class_wrapper


def with_dump(
    strip_nulls: bool = False,
    strip_privates: bool = False,
    strip_properties: bool = True,
    strip_class_variables: bool = True,
    strip_attr: Optional[Union[str, MutableSequence[str], tuple[str]]] = None,
    key_transformer: Optional[Callable[[str], str]] = None,
    verbose: Union[jsons.Verbosity, bool] = False,
    strict: bool = True,
) -> Callable[[T], T]:
    serializer = ClassSerializer(
        strip_nulls=strip_nulls,
        strip_privates=strip_privates,
        strip_properties=strip_properties,
        strip_class_variables=strip_class_variables,
        strip_attr=strip_attr,
        key_transformer=key_transformer,
        verbose=verbose,
        strict=strict,
    )

    return with_serializer(serializer=serializer)


def with_load(
    key_transformer: Optional[Callable[[str], str]] = None,
    strict: bool = True,
) -> Callable[[T], T]:
    deserializer = ClassDeserializer(
        key_transformer=key_transformer,
        strict=strict,
    )

    return with_deserializer(deserializer=deserializer)


def serializable(fork_inst: Type[StateHolder] = StateHolder) -> Callable[[T], T]:
    def class_wrapper(cls: T) -> T:
        jsons.set_serializer(
            _pop_serializer(cls),
            cls=cls,
            fork_inst=fork_inst
        )
        jsons.set_deserializer(
            _pop_deserializer(cls),
            cls=cls,
            fork_inst=fork_inst
        )

        return cls

    return class_wrapper


class Formatter(Generic[T], metaclass=abc.ABCMeta):
    def __init__(
        self,
        fork_inst: Type[StateHolder] = StateHolder
    ) -> None:
        self._fork_inst: Type[StateHolder] = fork_inst

    @abc.abstractmethod
    def _convert_obj_to_str(self, data: object) -> str:
        pass

    @abc.abstractmethod
    def _convert_str_to_obj(self, data: str) -> object:
        pass

    def dump(self, obj: T, **kwargs) -> object:
        return jsons.dump(obj, fork_inst=self._fork_inst, **kwargs)

    def load(self, obj: object, cls: Type[T], **kwargs) -> T:
        return jsons.load(obj, cls=cls, fork_inst=self._fork_inst, **kwargs)

    def dumps(self, obj: T, **kwargs) -> str:
        return self._convert_obj_to_str(self.dump(obj, **kwargs))

    def loads(self, obj: str, cls: Type[T], **kwargs) -> T:
        return self.load(self._convert_str_to_obj(data=obj), cls=cls, **kwargs)

    def dumpb(self, obj: T, encoding: str = "utf-8", **kwargs) -> bytes:
        return self.dumps(obj, **kwargs).encode(encoding=encoding)

    def loadb(self, obj: bytes, cls: Type[T], encoding: str = "utf-8", **kwargs) -> T:
        return self.loads(obj.decode(encoding=encoding), cls=cls, **kwargs)


class Parameters(object):
    def as_dict(self) -> dict:
        return {key: value for key, value in self.__dict__ if value is not None}


@dataclasses.dataclass
class JsonParameters(Parameters):
    skipkeys: Optional[bool] = None
    ensure_ascii: Optional[bool] = None
    check_circular: Optional[bool] = None
    allow_nan: Optional[bool] = None
    indent: Optional[int] = None
    separators: Optional[tuple[str]] = None
    default: Optional[callable] = None
    sort_keys: Optional[bool] = None


class JsonFormatter(Formatter[dict]):
    def __init__(
        self,
        parameters: JsonParameters = JsonParameters(),
        fork_inst: Type[StateHolder] = StateHolder
    ) -> None:
        super().__init__(fork_inst)

        self._parameters: JsonParameters = parameters

    def _convert_obj_to_str(self, data: object) -> str:
        return json.dumps(
            data,
            **cast(
                dict,
                jsons.dump(
                    self._parameters,
                    cls=JsonParameters,
                    strip_nulls=True,
                )
            )
        )

    def _convert_str_to_obj(self, data: str) -> object:
        return json.loads(
            data,
            **cast(
                dict,
                jsons.dump(
                    self._parameters,
                    cls=JsonParameters,
                    strip_nulls=True,
                )
            )
        )


@dataclasses.dataclass
class YamlParameters(Parameters):
    mapping: int = 4
    sequence: int = 4
    offset: int = 2


class YamlFormatter(Formatter[dict]):
    def __init__(
        self,
        parameters: YamlParameters = YamlParameters(),
        fork_inst: Type[StateHolder] = StateHolder
    ) -> None:
        super().__init__(fork_inst)

        self._parameters: YamlParameters = parameters

    def _convert_obj_to_str(self, data: object) -> str:
        yaml_container = io.StringIO()

        yaml = YAML()
        yaml.indent(
            mapping=self._parameters.mapping,
            sequence=self._parameters.sequence,
            offset=self._parameters.offset
        )
        yaml.dump(data=data, stream=yaml_container)

        return yaml_container.getvalue()

    def _convert_str_to_obj(self, data: str) -> object:
        return YAML(typ='safe').load(data)


class DataFormatter(object):
    def __init__(self, parameters: Optional[Parameters] = None) -> None:
        self._parameters: Optional[Parameters] = parameters


class QUOTING(enum.IntEnum):
    QUOTE_ALL = csv.QUOTE_ALL
    QUOTE_MINIMAL = csv.QUOTE_MINIMAL
    QUOTE_NONE = csv.QUOTE_NONE
    QUOTE_NONNUMERIC = csv.QUOTE_NONNUMERIC


@dataclasses.dataclass
class XSVParameters(Parameters):
    delimiter: Optional[str] = None
    doublequote: Optional[bool] = None
    escapechar: Optional[str] = None
    lineterminator: Optional[str] = None
    quotechar: Optional[str] = None
    quoting: Optional[QUOTING] = None
    skipinitialspace: Optional[bool] = None


class XSVDataFormatter(DataFormatter):
    def __init__(self, parameters: XSVParameters = XSVParameters()) -> None:
        super().__init__(parameters=parameters)

    def load_data(self, data: str) -> Iterable[Iterable[Any]]:
        reader = csv.reader(
            data.split(self._parameters.lineterminator),
            **self._parameters.as_dict()
        )

        return [line for line in reader if not (len(line) < 1)]

    def dump_data(self, data: Iterable[Iterable[Any]]) -> str:
        csv_container = io.StringIO()
        writer = csv.writer(csv_container, **self._parameters.as_dict())

        writer.writerows(data)

        return csv_container.getvalue()


@dataclasses.dataclass
class JsonDataFormatter(DataFormatter):
    def __init__(self, parameters: JsonParameters = JsonParameters()) -> None:
        super().__init__(parameters=parameters)

    def load_data(self, data: str) -> dict[str, Any]:
        return json.loads(data)

    def dump_data(self, data: dict[str, Any]) -> str:
        return json.dumps(data, **self._parameters.as_dict())


@dataclasses.dataclass
class YamlDataFormatter(DataFormatter):
    def __init__(self, parameters: YamlParameters = YamlParameters()) -> None:
        super().__init__(parameters=parameters)

    def load_data(self, data: str) -> dict[str, Any]:
        return YAML(typ='safe').load(data)

    def dump_data(self, data: dict[str, Any]) -> str:
        yaml_container = io.StringIO()

        yaml = YAML()
        yaml.indent(**self._parameters.as_dict())
        yaml.dump(data=data, stream=yaml_container)

        return yaml_container.getvalue()


@dataclasses.dataclass
class EnvDataFormatter(DataFormatter):
    def __init__(self) -> None:
        super().__init__(parameters=None)

    def load_data(self, data: str) -> dict[str, str]:
        # TODO: casting values (if needed)
        d = {}

        for line in data:
            line = line.strip()
            if not line.startswith('#') or line.strip() != "":
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if key == "":
                    raise ValueError("Invalid key")

                d[key] = value if value != "" else None

        return d

    def dump_data(self, data: dict[str, Any]) -> str:
        # TODO: handle space in strings
        s = ""

        for key, value in data.items():
            s += f"{key}={value}"

        return s
