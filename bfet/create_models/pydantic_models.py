from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..create_data.map_types.type_to_data import map_type_to_data

T = BaseModel
# T = TypeVar("T")


class PydanticTestingModel:
    def __init__(self, model: Type[T], fill_all_fields: bool) -> None:
        self.model: Type[T] = model
        self.fill_all_fields = fill_all_fields

    @classmethod
    def create(cls, model: Type[T], fill_all_fields: bool = False, **kwargs: Any) -> T:
        """The method to call when we want to create one or more instances
        TODO
        Create and raise an error if in_bulk or quantity > 1 and force_create is set to True
        and instances can't be created without repeating a given field

        Parameters
        ----------
            model : Type[T]
                The model that we want to use to create the instances from

            fill_all_fields : bool
                Boolean to tell if all the fields must be filled or it's better to leave them blank
                (if possible), by default False

            kwargs
                Fields of the model that we want to manually fill

        Returns
        -------
            T
                An object with the passed model
        """
        return cls(model, fill_all_fields)._create_model(kwargs)

    @classmethod
    def create_many(
        cls,
        model: Type[T],
        fill_all_fields: bool = False,
        number_of_models: int = 2,
        **kwargs,
    ) -> List[T]:
        """The method to call when we want to create more than one instance

        Parameters
        ----------
            model : Type[T]
                The model that we want to use to create the instances from

            number_of_models : int
                The number of instances that we want to create, by default 2

            fill_all_fields : bool
                Boolean to tell if all the fields must be filled or it's better to leave them blank
                (if possible), by default False

            kwargs
                Fields of the model that we want to manually fill

        Returns
        -------
            List[T]
                A list of models
        """
        creator = cls(model, fill_all_fields)
        return [creator._create_model(kwargs) for _ in range(number_of_models)]

    def _create_model(self, kwargs: Dict[str, Any]) -> T:
        fields = self.model.model_fields.items()
        data = dict(self._create_field(name, info, kwargs.get(name)) for name, info in fields)
        return self.model(**data)

    def _create_field(
        self,
        name: str,
        info: FieldInfo,
        default_data: Optional[Any],
    ) -> Tuple[str, Any]:
        return info.alias or name, default_data or self._inspect_field(info)

    def _inspect_field(self, info: FieldInfo) -> Any:
        if info.default_factory:
            return info.default_factory()
        return info.default or self._get_field_type_data(str(info.annotation))

    def _get_field_type_data(self, field_type: str) -> Dict:
        return map_type_to_data(field_type)
