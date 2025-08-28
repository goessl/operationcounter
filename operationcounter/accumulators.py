from functools import reduce
from operator import mul

__all__ = ('MISSING',
           'reduce_default', 'sum_default', 'prod_default', 'sumprod_default')



MISSING = object()
"""Sentinel to mark empty parameters."""

def reduce_default(function, iterable, *, initial=MISSING, default=0):
    """Apply function of two arguments cumulatively to the iterable.
    
    Like `functools.reduce` but with an optional initial element and an
    optional default return value.
    Difference to `functools.reduce`:
    - If `iterable` is empty and `initial` and `default` is `MISSING`, an
      `TypeError` is raised.
    - If `iterable` is empty and `initial` is `MISSING`, but `default` is not,
      then `default` is returned.
    """
    if initial is not MISSING:
        return reduce(function, iterable, initial)
    else:
        it = iter(iterable)
        try:
            initial = next(it)
        except StopIteration:
            if default is not MISSING:
                return default
            else:
                raise TypeError("accumulation of empty iterable with no" \
                        + " initial or default value")
        return reduce(function, it, initial)

def sum_default(iterable, *, initial=MISSING, default=0):
    """Return the sum of all elements in the iterable.
    
    Like `sum` but with an optional initial element and an optional default
    return value.
    - If `iterable` is empty and `initial` and `default` is `MISSING`, an
      `TypeError` is raised.
    - If `iterable` is empty and `initial` is `MISSING`, but `default` is not,
      then `default` is returned.
    - If `initial` is `MISSING`, then there is truly no initial `0 +=`.
    """
    if initial is not MISSING:
        return sum(iterable, initial)
    else:
        it = iter(iterable)
        try:
            initial = next(it)
        except StopIteration:
            if default is not MISSING:
                return default
            else:
                raise TypeError("accumulation of empty iterable with no" \
                        + " initial or default value")
        return sum(it, start=initial)

def prod_default(iterable, *, initial=MISSING, default=1):
    """Return the product of all elements in the iterable.
    
    Like `math.prod` but with an optional initial element and an optional
    default return value.
    - If `iterable` is empty and `initial` and `default` is `MISSING`, an
      `TypeError` is raised.
    - If `iterable` is empty and `initial` is `MISSING`, but `default` is not,
      then `default` is returned.
    - If `initial` is `MISSING`, then there is truly no initial `1 *=`.
    """
    #don't use math.prod, as it may reject non-numeric values
    return reduce_default(mul, iterable, initial=initial, default=default)

def sumprod_default(a, b, *, initial=MISSING, default=0):
    """Return the sum-product of all elements in the iterables.
    
    Like `math.sumprod` but with an optional initial element, an optional
    default return value and non-strict zipping of both iterables.
    - If `a` or `b` is empty and `initial` and `default` is `MISSING`, an
      `TypeError` is raised.
    - If `a` or `b` is empty and `initial` is `MISSING`, but `default` is not,
      then `default` is returned.
    - If `initial` is `MISSING`, then there is truly no initial `0 +=`.
    """
    return sum_default(map(mul, a, b), initial=initial, default=default)
