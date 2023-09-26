from enum import Enum
from itertools import chain, combinations, product
from random import choices, randrange

from typing import Callable, Deque, FrozenSet, Iterable, List, Set, Tuple, Any, Dict

AnySizedIterable = List[Any] | Set[Any] | FrozenSet[Any] | Tuple[Any] | Deque[Any]


def create_all_combinations(data: AnySizedIterable, minimum: int = 1) -> chain[Any]:
    return chain.from_iterable(combinations(data, i) for i in range(minimum, len(data) + 1))


def cast_all_combinations(
    data: AnySizedIterable,
    minimum: int = 1,
    cast_to: Callable[[chain[Any]], AnySizedIterable] = list,
) -> AnySizedIterable:
    return cast_to(create_all_combinations(data=data, minimum=minimum))


def create_possibilities(possibilities_per_field: Dict[str, List[Any]]) -> Iterable:
    return product(*iter(possibilities_per_field.values()))


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
    ) -> None:
        self.name = name
        self.options = options
        self.variations = variations
        self.number_of_variations = number_of_variations
        self.can_be_empty = can_be_empty
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

    def value(self) -> Dict[str, List[Any] | chain[Any]]:
        return {self.name: self._get_values()[self.variations]}

    def _get_values(self) -> Dict[Variations, List[Any] | chain[Any]]:
        empty_as_int = int(self.can_be_empty)
        all_combinations = create_all_combinations(self.options, empty_as_int)
        return {
            Variations.ANY: choices(all_combinations, randrange(empty_as_int)),  # type: ignore
            Variations.ALL: all_combinations,
            Variations.SOME: choices(all_combinations, self.number_of_variations),  # type: ignore
            Variations.EMPTY: [],
        }
