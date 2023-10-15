from __future__ import annotations

from collections import deque
from itertools import chain, product
from typing import Any, List

import pytest

from bfet.create_data.data_combination import (
    Combinator,
    Variations,
    cast_all_combinations,
    create_all_combinations,
    create_possibilities,
)


@pytest.mark.parametrize(
    "variation, expected_result",
    [
        (Variations.ALL, (4, 4)),
        (Variations.ANY, (0, 4)),
        (Variations.SOME, (5, 5)),
        (Variations.EMPTY, (0, 0)),
    ],
)
def test_combinator_value(variation: Variations, expected_result: List[Any]):
    combinator = Combinator(
        name="combi",
        options=[["cool"], ["very", "cool"]],
        variations=variation,
        number_of_variations=5,
        excluded_combinations=[],
    )
    result = combinator.value()
    assert isinstance(result, dict)
    assert "combi" in result
    low, high = expected_result
    assert low <= len(result["combi"]) <= high


@pytest.mark.parametrize("cast_to", [list, deque, tuple])
def test_cast_all_combinations(cast_to):
    result = cast_all_combinations([["cool"], ["very", "cool"]], cast_to=cast_to)
    assert isinstance(result, cast_to)


def test_create_all_combinations():
    result = create_all_combinations([["cool"], ["very", "cool"]], minimum=0)
    assert isinstance(result, chain)
    assert list(result) == [(), (["cool"],), (["very", "cool"],), (["cool"], ["very", "cool"])]


def test_create_possibilities():
    options = {
        "field1": [["cool"], ["very", "cool"]],
        "field2": ["hey", None],
        "field3": [1, 2, 3],
    }
    result = create_possibilities(options)
    assert isinstance(result, product)
    assert list(result) == [
        (["cool"], "hey", 1),
        (["cool"], "hey", 2),
        (["cool"], "hey", 3),
        (["cool"], None, 1),
        (["cool"], None, 2),
        (["cool"], None, 3),
        (["very", "cool"], "hey", 1),
        (["very", "cool"], "hey", 2),
        (["very", "cool"], "hey", 3),
        (["very", "cool"], None, 1),
        (["very", "cool"], None, 2),
        (["very", "cool"], None, 3),
    ]
