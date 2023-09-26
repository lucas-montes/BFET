from bfet import PydanticTestingModel

from ...pydantic_example import BaseTestModel


def test_create():
    result = PydanticTestingModel.create(BaseTestModel)


def test_get_field_type():
    BaseTestModel
