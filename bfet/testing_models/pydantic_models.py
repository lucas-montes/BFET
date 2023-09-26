from typing import Any, Dict, List, Tuple, Type, TypeVar

from ..create_data import (
    create_random_bool,
    create_random_date,
    create_random_datetime,
    create_random_email,
    create_random_float,
    create_random_hour,
    create_random_integer,
    create_random_json,
    create_random_positive_integer,
    create_random_slug,
    create_random_string,
    create_random_text,
    create_random_url,
    create_random_uuid,
)


from pydantic import BaseModel

T = BaseModel
# T = TypeVar("T")


class PydanticTestingModel:
    def __init__(self, model: Type[T], fill_all_fields: bool) -> None:
        self.model = model
        self.fill_all_fields = fill_all_fields

    @classmethod
    def create(cls, model: Type[T], fill_all_fields: bool = False, **kwargs: Any) -> T:
        """The method to call when we want to create one or more instances
        TODO
        Create and raise an error if in_bulk or quantity > 1 and force_create is set to True
        and instances can't be created without repeating a given field

        Parameters
        ----------
            model : Type
                The model that we want to use to create the instances from

            fill_all_fields : bool
                Boolean to tell if all the fields must be filled or it's better to leave them blank
                (if possible), by default False

            kwargs
                Fields of the model that we want to manually fill

        Returns
        -------
            Type
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
            model : Type
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
            List[Type]
                A list of models
        """
        creator = cls(model, fill_all_fields)
        return [creator._create_model(kwargs) for _ in range(number_of_models)]

    def _create_model(self, kwargs: Dict[str, Any]) -> Any:
        fields = self.model.model_fields.items()
        data = dict(self._inspect_field(field) for field in fields)
        return self.model(**data)

    def _inspect_field(self, kwargs: Dict[str, Any]) -> Tuple[str, Any]:
        return

    def _match_field_type(self, field_type: str) -> Dict:
        return field_type
