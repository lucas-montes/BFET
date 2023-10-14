from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field


def default_factory():
    return 25


class BaseTestModel(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]
    default_function: int = Field(default_factory=default_factory)
    default_value: int = Field(alias="DefaultValueAlias", default=33)
