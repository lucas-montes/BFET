from typing import Any, Dict, List, Optional, Type, TypeVar

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

T = TypeVar("T")


class DjangoTestingModel:
    def __init__(
        self,
        model,
        quantity: int,
        in_bulk: bool,
        fill_all_fields: bool,
        force_create: bool,
    ) -> None:
        self.model = model
        self.quantity = quantity
        self.in_bulk = in_bulk
        self.fill_all_fields = fill_all_fields
        self.force_create = force_create

    @classmethod
    def create(
        cls,
        model: Type[T],
        fill_all_fields: bool = True,
        force_create: bool = False,
        **kwargs: Any,
    ) -> T:
        """The method to call when we want to create one or more instances
        TODO
        Create and raise an error if in_bulk or quantity > 1 and force_create is set to True
        and instances can't be created without repeating a given field

        Parameters
        ----------
            model : Type
                The model that we want to use to create the instances from

            quantity : int, optional
                The number of instances that we want to create, by default 1

            in_bulk : bool, optional
                Boolean to use the bulk_create built-in of Django, by default False

            fill_all_fields : bool, optional
                Boolean to tell if all the fields must be filled or it's better to leave them blank
                (if possible), by default True

            force_create : bool, optional
                Boolean to indicate, if any field is manually filled, it has to perform
                a get_or_create instead of create, by default False

            kwargs
                Fields of the model that we want to manually fill

        Returns
        -------
            Union[Type, List[Type]]
                An instance or a list of instances created
        """
        return cls(
            model=model,
            quantity=1,
            in_bulk=False,
            fill_all_fields=fill_all_fields,
            force_create=force_create,
        ).create_model(**kwargs)

    @classmethod
    def create_many(
        cls,
        model: Type[T],
        quantity: int = 2,
        in_bulk: bool = False,
        fill_all_fields: bool = True,
        force_create: bool = False,
        **kwargs,
    ) -> List[T]:
        """The method to call when we want to create one or more instances
        TODO
        Create and raise an error if in_bulk or quantity > 1 and force_create is set to True
        and instances can't be created without repeating a given field

        Parameters
        ----------
            model : Type
                The model that we want to use to create the instances from

            quantity : int, optional
                The number of instances that we want to create, by default 1

            in_bulk : bool, optional
                Boolean to use the bulk_create built-in of Django, by default False

            fill_all_fields : bool, optional
                Boolean to tell if all the fields must be filled or it's better to leave them blank
                (if possible), by default True

            force_create : bool, optional
                Boolean to indicate, if any field is manually filled, it has to perform
                a get_or_create instead of create, by default False

            kwargs
                Fields of the model that we want to manually fill

        Returns
        -------
            Union[Type, List[Type]]
                An instance or a list of instances created
        """
        if in_bulk:
            return cls(
                model,
                quantity,
                in_bulk,
                fill_all_fields,
                force_create,
            ).create_in_bulk(**kwargs)
        return [
            cls(
                model,
                quantity,
                in_bulk,
                fill_all_fields,
                force_create,
            ).create_model(**kwargs)
            for _ in range(quantity)
        ]

    def get_model_manager(self) -> Type:
        try:
            manager = self.model._default_manager
        except AttributeError:
            manager = self.model.objects
        return manager

    def create_in_bulk(self, **kwargs):
        pre_objects = [
            self.model(
                **self.inspect_model(**kwargs),
            )
            for _ in range(self.quantity)
        ]
        return self.get_model_manager().bulk_create(pre_objects)

    def create_model(self, **kwargs):
        model_data = self.inspect_model(**kwargs)
        model_manager = self.get_model_manager()
        if self.force_create:
            kwargs |= model_data
            model = model_manager.create(**kwargs)
        elif model_manager.filter(**kwargs).exists():
            model = model_manager.filter(**kwargs).first()
        else:
            model, _ = model_manager.get_or_create(
                **kwargs,
                defaults=model_data,
            )
        return model

    def inspect_model(self, **kwargs) -> Dict:
        fields_info = {}
        for field in self.model._meta.fields:
            field_name = field.name
            if field_name == "id":
                continue
            if field_name in kwargs:
                fields_info[field_name] = kwargs.pop(field_name)
            else:
                if self.fill_all_fields is False and field.__dict__.get("null"):
                    fields_info[field_name] = None
                    continue

                fields_info |= self.inspect_field(field, field_name)

        return fields_info

    @staticmethod
    def set_max_value(max_length: Optional[int | float]) -> int:
        max_length = max_length or 10
        if max_length > 1000:
            max_length = max_length / 100
        elif max_length > 100:
            max_length = max_length / 10
        return int(max_length)

    def inspect_field(self, field: Type, field_name: str) -> Dict:
        field_info = field.__dict__
        extra_params = {}
        if max_lenght := field_info.get("max_length"):
            extra_params = {"max_value": self.set_max_value(max_lenght)}
        return {
            field_name: self.generate_random_data_per_field(
                field.get_internal_type(),
                extra_params,
            )
        }

    def generate_random_data_per_field(
        self,
        field_type: str,
        extra_params,
    ):
        # BigIntegerField (min_value=10000)
        # PositiveBigIntegerField (min_value=10000)
        data_generator = {
            "DateTimeField": create_random_datetime,
            "DateField": create_random_date,
            "TimeField": create_random_hour,
            # "DurationField": DjangoTestingModel.create(),
            # "AutoField": DjangoTestingModel.create(),
            # "BigAutoField": DjangoTestingModel.create(),
            # "SmallAutoField": DjangoTestingModel.create(),
            # "BinaryField": DjangoTestingModel.create(),
            # "CommaSeparatedIntegerField": DjangoTestingModel.create(),
            "DecimalField": create_random_float,
            "FloatField": create_random_float,
            "BigIntegerField": create_random_integer,
            "PositiveBigIntegerField": create_random_positive_integer,
            "PositiveIntegerField": create_random_positive_integer,
            "PositiveSmallIntegerField": create_random_positive_integer,
            "IntegerField": create_random_integer,
            "SmallIntegerField": create_random_integer,
            "CharField": create_random_string,
            "TextField": create_random_text,
            "SlugField": create_random_slug,
            "URLField": create_random_url,
            "UUIDField": create_random_uuid,
            "EmailField": create_random_email,
            # "Empty": DjangoTestingModel.create(),
            # "Field": DjangoTestingModel.create(),
            # "NOT_PROVIDED": DjangoTestingModel.create(),
            # "FilePathField": DjangoTestingModel.create(),
            "FileField": self.return_none_by_now,
            "ImageField": self.return_none_by_now,
            "JSONField": create_random_json,
            # "GenericIPAddressField": DjangoTestingModel.create(),
            # "IPAddressField": DjangoTestingModel.create(),
            "BooleanField": create_random_bool,
            "NullBooleanField": create_random_bool,
            "ForeignKey": self.return_none_by_now,
            "OneToOneField": self.return_none_by_now,
            "ManyToManyField": self.return_none_by_now,
        }
        return data_generator[field_type](**extra_params)  # type: ignore

    def return_none_by_now(self, **extra_params):
        return None
