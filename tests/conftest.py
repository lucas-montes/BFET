from __future__ import annotations

from datetime import datetime
import os
from typing import Tuple

import django
from django.conf import settings

from bfet.testing.compare_services import ServiceRequest


def mock_service_requests() -> Tuple[ServiceRequest, ServiceRequest]:
    service_request1 = ServiceRequest(
        start_datetime=datetime(2023, 10, 15, 13, 23, 46, 252402),
        execution_time=382.17878341674805,
        response="",
    )
    service_request2 = ServiceRequest(
        start_datetime=datetime(2023, 10, 15, 13, 23, 46, 251536),
        execution_time=387.10975646972656,
        response="",
    )
    return service_request1, service_request2


def pytest_configure():
    test_db = os.environ.get("TEST_DB", "sqlite")
    installed_apps = [
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "tests.django_examples",
    ]

    using_postgres_flag = False
    postgis_version = ()
    if test_db == "sqlite":
        db_engine = "django.db.backends.sqlite3"
        db_name = ":memory:"
        extra_db_name = ":memory:"
    elif test_db == "postgresql":
        using_postgres_flag = True
        db_engine = "django.db.backends.postgresql_psycopg2"
        db_name = "postgres"
        installed_apps = ["django.contrib.postgres"] + installed_apps
        extra_db_name = "extra_db"
    elif test_db == "postgis":
        using_postgres_flag = True
        db_engine = "django.contrib.gis.db.backends.postgis"
        db_name = "postgres"
        extra_db_name = "extra_db"
        installed_apps = [
            "django.contrib.postgres",
            "django.contrib.gis",
        ] + installed_apps
        postgis_version = (11, 3, 0)
    else:
        raise NotImplementedError("Tests for % are not supported", test_db)

    extra_db = "extra"
    settings.configure(
        EXTRA_DB=extra_db,
        DATABASES={
            "default": {
                "ENGINE": db_engine,
                "NAME": db_name,
                "HOST": "localhost",
                # The following DB settings are only used for `postgresql` and `postgis`
                "PORT": os.environ.get("PGPORT", ""),
                "USER": os.environ.get("PGUSER", ""),
                "PASSWORD": os.environ.get("PGPASSWORD", ""),
            },
            # Extra DB used to test multi database support
            extra_db: {
                "ENGINE": db_engine,
                "NAME": extra_db_name,
                "HOST": "localhost",
                "PORT": os.environ.get("PGPORT", ""),
                "USER": os.environ.get("PGUSER", ""),
                "PASSWORD": os.environ.get("PGPASSWORD", ""),
            },
        },
        INSTALLED_APPS=installed_apps,
        LANGUAGE_CODE="en",
        SITE_ID=1,
        MIDDLEWARE=(),
        USE_TZ=os.environ.get("USE_TZ", True),
        USING_POSTGRES=using_postgres_flag,
        # Set the version explicitly otherwise Django does extra queries
        # to get the version via SQL when using POSTGIS
        POSTGIS_VERSION=postgis_version,
    )

    django.setup()
