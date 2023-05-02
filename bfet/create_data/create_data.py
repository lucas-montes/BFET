import datetime
import random
import string
import textwrap
from typing import Dict, Optional
import uuid

from .constants import LIST_EMAIL_DOMAINS, LOREM_TEXT


def create_random_string(
    max_value: int = 100,
    use_punctuation: bool = False,
    use_digits: bool = True,
) -> str:
    min_value = 50
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_punctuation:
        characters += string.punctuation
    if max_value < min_value:
        min_value += max_value - min_value
    number = random.randint(min_value, max_value)
    return "".join(random.choice(characters) for _ in range(number))


def create_random_text(max_value: int = 50) -> str:
    return textwrap.wrap(LOREM_TEXT, max_value)[0]


def create_random_bool() -> bool:
    return random.randint(0, 1) == 1


def create_random_json() -> Dict:
    choices = {
        1: create_random_string(),
        2: create_random_bool(),
        3: create_random_datetime().strftime(
            "%m/%d/%Y, %H:%M:%S",
        ),
        4: create_random_float(),
    }
    return {choices[random.randint(1, 4)]: choices[random.randint(1, 4)] for _ in range(3)}


def create_random_slug(
    max_value: int = 50,
    use_digits: bool = True,
) -> str:
    return "-".join(
        [
            create_random_string(
                max_value=max_value,
                use_punctuation=False,
                use_digits=use_digits,
            )
            for _ in range(4)
        ]
    )[:max_value]


def create_random_email(max_value: int = 25) -> str:
    email_name = create_random_string(max_value)
    email_domain = random.choice(LIST_EMAIL_DOMAINS)
    return f"{email_name}@{email_domain}"


def create_random_url(max_value: int = 20, secure=True) -> str:
    domain = create_random_string(max_value)
    top_level_domain = random.choice(LIST_EMAIL_DOMAINS).split(".")[-1]
    protocol = "https" if secure else "http"
    return f"{protocol}://{domain}.{top_level_domain}"


def create_random_uuid(kind: int = 4, **kwargs) -> uuid.UUID:
    # TODO fix and do a better implementation
    uuids = {
        1: uuid.uuid1,
        3: uuid.uuid3,
        4: uuid.uuid4,
        5: uuid.uuid5,
    }
    if kind == 4:
        return uuids[kind]()  # type: ignore
    if ("namespace" or "name") in kwargs:
        return uuids[kind](**kwargs)  # type: ignore
    try:
        final_uuid = uuids[kind](**kwargs)  # type: ignore
    except Exception:
        final_uuid = uuids[kind]()  # type: ignore
    return final_uuid


def create_random_date(
    day: Optional[int] = None,  # type: ignore
    month: Optional[int] = None,  # type: ignore
    year: Optional[int] = None,  # type: ignore
) -> datetime.date:
    month = month or random.randint(1, 12)
    if month == 2:
        max_day = 28
    elif month in {1, 3, 5, 7, 8, 10, 12}:
        max_day = 31
    else:
        max_day = 30
    day = day or random.randint(1, max_day)
    year = year or random.randint(1900, 2100)
    return datetime.date(
        year=year,
        month=month,
        day=day,
    )


def create_random_hour(
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    second: Optional[int] = None,
    microsecond: Optional[int] = None,
    tzinfo: datetime.timezone = datetime.timezone.utc,
) -> datetime.time:
    hour = hour or random.randint(0, 23)
    minute = minute or random.randint(0, 59)
    second = second or random.randint(0, 59)
    microsecond = microsecond or random.randint(0, 59)
    return datetime.time(
        hour,
        minute,
        second,
        microsecond,
        tzinfo,
    )


def create_random_datetime(
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    second: Optional[int] = None,
    microsecond: Optional[int] = None,
    tzinfo: datetime.timezone = datetime.timezone.utc,
) -> datetime.datetime:
    date = create_random_date(
        day=day,
        month=month,
        year=year,
    )
    time = create_random_hour(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
        tzinfo=tzinfo,
    )
    return datetime.datetime.combine(
        date=date,
        time=time,
        tzinfo=tzinfo,
    )


def create_random_integer(
    min_value: int = 0,
    max_value: int = 10000000,
) -> int:
    if max_value < min_value:
        min_value += max_value - min_value
    fnct = random.choice(
        [
            create_random_negative_integer,
            create_random_positive_integer,
        ]
    )
    return fnct(min_value, max_value)


def create_random_negative_integer(
    min_value: int = 0,
    max_value: int = 10000000,
) -> int:
    return random.randint(min_value, max_value) * -1


def create_random_positive_integer(
    min_value: int = 0,
    max_value: int = 10000000,
) -> int:
    return random.randint(min_value, max_value)


def create_random_float(
    min_value: float = 0, max_value: float = 10000000, after_coma: int = 2
) -> float:
    if max_value < min_value:
        min_value += max_value - min_value
    fnct = random.choice(
        [
            create_random_negative_float,
            create_random_positive_float,
        ]
    )
    return fnct(min_value, max_value, after_coma)


def create_random_positive_float(
    min_value: float = 0,
    max_value: float = 10000000,
    after_coma: int = 2,
) -> float:
    return round(random.uniform(min_value, max_value), after_coma)


def create_random_negative_float(
    min_value: float = 0,
    max_value: float = 10000000,
    after_coma: int = 2,
) -> float:
    return round(random.uniform(min_value, max_value), after_coma) * -1
