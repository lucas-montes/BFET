import pytest

from bfet import DjangoTestingModel

from ...django_examples.models import FKTestingModel


@pytest.mark.django_db
class TestDjangoTestingModel:
    def test_make_should_create_one_object(self):
        new_obj = DjangoTestingModel.create(FKTestingModel)
        assert isinstance(new_obj, FKTestingModel)

    def create_check_model(self) -> FKTestingModel:
        assert FKTestingModel.objects.all().count() == 0
        new_obj: FKTestingModel = DjangoTestingModel.create(
            FKTestingModel,
            name="prueba",
        )
        assert FKTestingModel.objects.all().count() == 1
        assert new_obj.name == "prueba"
        return new_obj

    def test_model_create(self):
        self.create_check_model()

    def test_model_get_or_create(self):
        new_obj = self.create_check_model()
        duplicated_obj = DjangoTestingModel.create(
            FKTestingModel,
            name="prueba",
        )
        assert new_obj == duplicated_obj

    def test_max_lenght(self):
        new_obj: FKTestingModel = DjangoTestingModel.create(FKTestingModel)
        assert len(new_obj.name) <= 32
