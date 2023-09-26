from datetime import datetime

from pydantic import BaseModel, PositiveInt


class BaseTestModel(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]
