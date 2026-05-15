"""operationcounter.iterators module.

Iterators.
"""



from typing import Any, Never
from collections.abc import Iterable, Generator



def exception_generator(ex:type[Exception]=IndexError) -> Generator[Never]:
    """Raise the provided exception on the first yield.
    
    ```python
    >>> sum(islice(chain([1, 2, 3], exception_generator()), 3))
    6
    >>> sum(islice(chain([1, 2, 3], exception_generator()), 4))
    Traceback (most recent call last):
      ...
    IndexError
    ```
    
    Used to ensure that iteration doesn't go too far.
    """
    def raiser():
        raise ex
    return iter(raiser, object())

def group_ordinal(*iterables:Iterable[Any]) -> tuple[Any,...]:
    """Group elements of iterables by their ordinal.
    
    ```python
    >>> iterables = (1, 2, 3), [4, 5, 6, 7], {8}
    >>> list(group_ordinal(*iterables))
    [(1, 4, 8), (2, 5), (3, 6), (7,)]
    ```
    
    The elements are grouped in the same order as their iterables (stable).
    
    References
    ----------
    - [more-itertools PR #1073](https://github.com/more-itertools/more-itertools/pull/1073)
    """
    iterators = list(map(iter, reversed(iterables)))
    result = []
    while iterators:
        result.clear()
        for i in reversed(range(len(iterators))):
            try:
                result.append(next(iterators[i]))
            except StopIteration:
                del iterators[i]
        if result:
            yield tuple(result)
