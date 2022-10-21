from bfet import DjangoTestingModel

from django.test import TestCase
from django.db import models


class BarModel(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    non_filled = models.CharField(
        max_length=32,
    )


class TestExample(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        bar_model_autofilled = DjangoTestingModel.create(BarModel)
        bar_model_partially_filled = DjangoTestingModel.create(BarModel, name="some")
        bar_model_completly_filled = DjangoTestingModel.create(
            BarModel, name="some", non_filled="other"
        )
