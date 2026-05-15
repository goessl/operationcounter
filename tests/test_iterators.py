from operationcounter import *
from itertools import islice, chain
import pytest


def test_exception_generator():
    assert sum(islice(chain([1, 2, 3], exception_generator()), 3)) == 6
    with pytest.raises(IndexError):
        sum(islice(chain([1, 2, 3], exception_generator()), 4))

def test_group_ordinal():
    iterables = (
        (1, 2, 3),
        [4, 5, 6, 7],
        {8}
    )
    expected = [
        (1, 4, 8),
        (2, 5),
        (3, 6),
        (7,)
    ]
    assert list(group_ordinal(*iterables)) == expected
    #empty case
    assert list(group_ordinal()) == []
