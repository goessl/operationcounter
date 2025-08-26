from functools import reduce
from operator import mul

__all__ = ('reduce_default', 'sum_default', 'prod_default', 'sumprod_default')



def reduce_default(function, iterable, default=0):
    """Apply function of two arguments cumulatively to the items of iterable.
    
    Like `functools.reduce` but without the function applied to some initial
    element and the first element in the iterable. Returns `default` if
    `iterable` is empty.
    """
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        return default
    return reduce(function, it, first)

def sum_default(iterable, default=0):
    """Return the sum of all elements in iterable.
    
    Like `sum` but without the default initial `0+`. Returns `default` if
    `iterable` is empty.
    """
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        return default
    return sum(it, start=first)

def prod_default(iterable, default=1):
    """Return the product of all elements in iterable.
    
    Like `math.prod` but without the default initial `1*`. Returns `default`
    if `iterable` is empty.
    """
    #don't use math.prod, as it may reject non-numeric values
    return reduce_default(mul, iterable, default)

def sumprod_default(a, b, default=0):
    """Return the sum-product of all elements in the iterables.
    
    Like `math.sumprod` but without the default initial `0+`. Returns `default`
    if any iterable is empty. Zips both iterables, so they can be of different
    length.
    """
    return sum_default(map(mul, a, b), default)
