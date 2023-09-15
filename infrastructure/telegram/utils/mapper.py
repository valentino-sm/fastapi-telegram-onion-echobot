import sys
from importlib import import_module
from os import listdir
from os.path import isfile, join
from typing import Any, Generic, Mapping, TypeVar

from pydantic import ValidationError

from infrastructure.telegram.repositories.mapper import MapperRepository
from infrastructure.telegram.utils.exceptions import (UnknownMapperException,
                                                      UnsuccessMapperException)

path = "infrastructure/telegram/mappers"
abs_path = join(sys.path[0], path)

T = TypeVar("T")


class Mapper(Generic[T]):
    modules: dict[str, MapperRepository[T]] = {
        k.split(".")[0]: import_module(
            f"{path.replace('/', '.')}.{k.split('.')[0]}"
        ).Mapper
        for k in listdir(abs_path)
        if isfile(join(abs_path, k))
    }

    @classmethod
    def to_domain(cls, update_type: str, raw_update_obj: Mapping[Any, Any]) -> T:
        if update_type not in cls.modules:
            raise UnknownMapperException(update_type, raw_update_obj)

        try:
            result = cls.modules[update_type].to_domain(raw_update_obj)
        except (TypeError, KeyError, AttributeError, ValidationError) as e:
            raise UnsuccessMapperException(e, update_type, raw_update_obj) from e

        return result

    # from dataclasses import asdict
    # def to_dto(self, obj: Any) -> Mapping[Any, Any]:
    #     try:
    #         return asdict(obj)
    #     except TypeError:
    #         # TODO
    #         raise
