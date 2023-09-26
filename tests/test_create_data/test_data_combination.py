from bfet import Combinator, cast_all_combinations, create_all_combinations


def test_Combinator():
    result = Combinator()
    assert 1 == result


def test_cast_all_combinations():
    result = cast_all_combinations()
    assert isinstance(result, list)


def test_create_all_combinations():
    result = create_all_combinations()
    assert 1 == result
