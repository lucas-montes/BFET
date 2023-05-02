#!/usr/bin/env python

import datetime
import uuid

from bfet import (
    create_random_bool,
    create_random_date,
    create_random_datetime,
    create_random_email,
    create_random_float,
    create_random_hour,
    create_random_integer,
    create_random_json,
    create_random_negative_float,
    create_random_negative_integer,
    create_random_positive_float,
    create_random_positive_integer,
    create_random_slug,
    create_random_string,
    create_random_text,
    create_random_url,
    create_random_uuid,
)


def test_create_random_string():
    assert type(create_random_string()) == str


def test_create_random_text():
    assert type(create_random_text()) == str


def test_create_random_bool():
    assert type(create_random_bool()) == bool


def test_create_random_json():
    assert type(create_random_json()) == dict


def test_create_random_slug():
    assert type(create_random_slug()) == str


def test_create_random_email():
    assert type(create_random_email()) == str


def test_create_random_url():
    assert type(create_random_url()) == str


def test_create_random_uuid():
    kwargs = {"namespace": uuid.NAMESPACE_DNS, "name": "name"}
    assert type(create_random_uuid(1)) == uuid.UUID
    assert type(create_random_uuid(3, **kwargs)) == uuid.UUID
    assert type(create_random_uuid(4)) == uuid.UUID
    assert type(create_random_uuid(5, **kwargs)) == uuid.UUID


def test_create_random_date():
    assert type(create_random_date()) == datetime.date


def test_create_random_hour():
    assert type(create_random_hour()) == datetime.time


def test_create_random_datetime():
    assert type(create_random_datetime()) == datetime.datetime


def test_create_random_integer():
    assert type(create_random_integer()) == int


def test_create_random_negative_integer():
    assert type(create_random_negative_integer()) == int


def test_create_random_positive_integer():
    assert type(create_random_positive_integer()) == int


def test_create_random_float():
    assert type(create_random_float()) == float


def test_create_random_positive_float():
    assert type(create_random_positive_float()) == float


def test_create_random_negative_float():
    assert type(create_random_negative_float()) == float
