from __future__ import annotations

from unittest.mock import MagicMock, patch

from ...pydantic_example import BaseTestModel
from bfet.create_models.pydantic_models import PydanticTestingModel

TestModel = PydanticTestingModel(model=BaseTestModel, fill_all_fields=False)


def test_create():
    PydanticTestingModel.create(BaseTestModel)


def test_create_model():
    expected = {
        "id": "",
        "name": "",
        "signup_ts": "",
        "tastes": "",
    }
    result = PydanticTestingModel(model=BaseTestModel, fill_all_fields=True)._create_model(expected)

    assert isinstance(result, BaseTestModel)
    assert all(value == getattr(result, key) for key, value in expected)


def test_create_field_default():
    field = dict(BaseTestModel.model_fields.items())["id"]
    assert TestModel._create_field("name", field, "default") == "name", "default"


def test_create_field_alias():
    field = dict(BaseTestModel.model_fields.items())["default_value"]
    result = TestModel._create_field("name", field, "default")
    assert result == "DefaultValueAlias", "default"


@patch("bfet.create_models.pydantic_models.PydanticTestingModel._inspect_field")
def test_create_field(inspect_field: MagicMock):
    field = dict(BaseTestModel.model_fields.items())["id"]
    assert TestModel._create_field("name", field, None) == "name", inspect_field.return_value
    inspect_field.assert_called_once_with(field)


@patch("bfet.create_models.pydantic_models.PydanticTestingModel._get_field_type_data")
def test_inspect_field_use_random_data(get_field_type_data: MagicMock):
    field = dict(BaseTestModel.model_fields.items())["id"]
    result = TestModel._inspect_field(field)
    get_field_type_data.assert_called_once_with("int")
    assert result == get_field_type_data.return_value


@patch("bfet.create_models.pydantic_models.PydanticTestingModel._get_field_type_data")
def test_inspect_field_use_fields_default(get_field_type_data: MagicMock):
    field = dict(BaseTestModel.model_fields.items())["default_value"]
    result = TestModel._inspect_field(field)
    get_field_type_data.assert_not_called()
    assert result == 33


@patch("bfet.create_models.pydantic_models.PydanticTestingModel._get_field_type_data")
def test_inspect_field_use_fields_default_factory(get_field_type_data: MagicMock):
    field = dict(BaseTestModel.model_fields.items())["default_function"]
    result = TestModel._inspect_field(field)
    get_field_type_data.assert_not_called()
    assert result == 25


@patch("bfet.create_data.map_types.type_to_data.map_type_to_data")
def test_get_field_type_data_pydantic_type(map_type_to_data: MagicMock):
    result = TestModel._get_field_type_data("PositiveInt")
    map_type_to_data.assert_called_once_with()
    assert isinstance(result, int)


@patch("bfet.create_data.map_types.type_to_data.map_type_to_data")
def test_get_field_type_data_generic_type(map_type_to_data: MagicMock):
    result = TestModel._get_field_type_data("list")
    map_type_to_data.assert_called_once_with("list")
    assert isinstance(result, list)
