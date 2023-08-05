from __future__ import annotations

from dataclasses import is_dataclass
from enum import Enum
from typing import (Dict, TYPE_CHECKING, Any, List, Literal, Optional,
                    Union)

from .base_handler import BasicHandler, ClassHandler, TypeStoreType
from .named_types import NamedLiteral, NamedUnion


# Union is not really a type
class UnionHandler(BasicHandler[Any, TypeStoreType]):
    def should_handle(self, cls, origin, args) -> bool:
        return origin in (NamedUnion, Union)


class LiteralHandler(BasicHandler[Any, TypeStoreType]):
    def should_handle(self, cls, origin, args) -> bool:
        return origin in (Literal, NamedLiteral)


class EnumHandler(ClassHandler[Any, TypeStoreType]):
    def should_handle(self, cls: type, origin, args) -> bool:
        return issubclass(cls, Enum)


class DataclassHandler(ClassHandler[Any, TypeStoreType]):
    def is_mapping(self) -> bool:
        return True

    def should_handle(self, cls: type, origin, args) -> bool:
        return is_dataclass(cls)


class TupleHandler(BasicHandler[Any, TypeStoreType]):
    def should_handle(self, cls: Any, origin: Optional[type], args: List[Any]) -> bool:
        return origin is tuple


class ArrayHandler(BasicHandler[Any, TypeStoreType]):
    def should_handle(self, cls: Any, origin: Optional[type], args: List[Any]) -> bool:
        return origin == list and len(args) == 1


class MappingHandler(BasicHandler[Any, TypeStoreType]):
    def should_handle(self, cls: Any, origin: Optional[type], args: List[Any]) -> bool:
        return origin == dict and len(args) == 2
