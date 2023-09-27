from enum import Enum
from itertools import chain, combinations, product
from random import choices, randrange

from typing import (
    Callable,
    Deque,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Any,
    Dict,
)

AnySizedIterable = List[Any] | Set[Any] | FrozenSet[Any] | Tuple[Any] | Deque[Any]
CastableIterable = List[Any] | Tuple[Any] | Deque[Any]


def create_all_combinations(data: AnySizedIterable, minimum: int = 1) -> chain[Any]:
    return chain.from_iterable(combinations(data, i) for i in range(minimum, len(data) + 1))


def cast_all_combinations(
    data: AnySizedIterable,
    minimum: int = 1,
    cast_to: Callable[[chain[Any]], CastableIterable] = list,
) -> CastableIterable:
    return cast_to(create_all_combinations(data=data, minimum=minimum))


def create_possibilities(data: Dict[str, List[Any]]) -> Iterable:
    return product(*iter(data.values()))


class Variations(Enum):
    ANY = "ANY"
    ALL = "ALL"
    SOME = "SOME"
    EMPTY = "EMPTY"


class Combinator:
    def __init__(
        self,
        name: str,
        options: List[Any],
        variations: Variations = Variations.ALL,
        number_of_variations: int = 0,
        can_be_empty: bool = True,
        excluded_combinations: Optional[List[Any]] = None,
        cast_to: Callable[[chain[Any]], CastableIterable] = list,
    ) -> None:
        """

        Depending on what variation you select, you will have more or less values.
        If you pass options=[["cool"], ["very", "cool"]], you will have a total of 4 variations.
        Selecting Variations.ALL will return all 4 variations. Nevertheless, if you go with
        Variations.SOME and set number_of_variations to a number higher than 4, you will have more
        than 4 results that may be duplicated.
        """
        self.name = name
        self.options = options
        self.variations = variations
        self.number_of_variations = number_of_variations
        self.can_be_empty = can_be_empty
        self.excluded_combinations = excluded_combinations
        self.cast_to = cast_to
        self._validate()

    def _validate(self) -> None:
        if self.variations == Variations.EMPTY:
            print("number_of_variations and can_be_empty will be set to 0 and True")
            self.number_of_variations = 0
            self.can_be_empty = True
        elif self.variations == Variations.ALL:
            print("number_of_variations and can_be_empty will be set to len(self.options) and True")
            self.number_of_variations = len(self.options)
            self.can_be_empty = True
        elif self.number_of_variations < 1:
            raise ValueError("If we want some variations, number_of_variations should be >=1")
        return None

    def value(self) -> Dict[str, CastableIterable]:
        return {self.name: self._get_values()[self.variations]}

    def _get_values(self) -> Dict[Variations, CastableIterable]:
        empty_as_int = 0 if self.can_be_empty else 1
        all_combinations = cast_all_combinations(self.options, empty_as_int, self.cast_to)
        return {
            Variations.ANY: choices(
                all_combinations,
                k=randrange(empty_as_int, len(all_combinations)),
            ),
            Variations.ALL: all_combinations,
            Variations.SOME: choices(all_combinations, k=self.number_of_variations),
            Variations.EMPTY: [],
        }
