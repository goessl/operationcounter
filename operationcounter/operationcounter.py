import operator
from collections import Counter
from contextlib import contextmanager
from typing import Any, ClassVar, Generic, Optional, overload, TypeVar
from collections.abc import Collection, Generator, Mapping, Set, Sequence

__all__ = ('OperationCounter', 'count_ops')



T = TypeVar('T')

class OperationCounter(Generic[T]):
    """Wrap a value and count the operations performed on it.
    
    All arithmetic, bitwise, and comparison operations are intercepted and
    counted.
    """
    
    
    counter:ClassVar[Counter[str]] = Counter()
    """Live global counter of all operations."""
    
    def __init__(self, v:T) -> None:
        """Wrap `v` into an `OperationCounter`."""
        self.v:T = v
    
    
    # --- utilities ---
    @staticmethod
    def reset() -> None:
        """Clear all recorded operation counts."""
        OperationCounter.counter.clear()
    
    @staticmethod
    def snapshot() -> Counter[str]:
        """Return a copy of the current operation counts."""
        return OperationCounter.counter.copy()
    
    
    @staticmethod
    def wrap(x:T) -> OperationCounter[T]:
        """Wrap `v` into an `OperationCounter`.
        
        Same as `OperationCounter(x)`.
        """
        return OperationCounter(x)
    
    @staticmethod
    def wrapCollection(s:Collection[T]) -> Collection[OperationCounter[T]]:
        """Wrap the elements of `s` into `OperationCounter`s."""
        if isinstance(s, Mapping):
            return type(s)(
                    (OperationCounter.wrap(k), OperationCounter.wrap(v))
                    for k, v in s.items())
        elif isinstance(s, (Set, Sequence)):
            return type(s)(map(OperationCounter.wrap, s))
        else:
            raise TypeError(f'Unsupported type: {type(s)}')
    
    @staticmethod
    def wrapArray(a:Any) -> Any:
        """Return `np.ndarray(a)` with all elements wrapped."""
        try:
            import numpy as np
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                'OperationCounter.wrapArray requires `numpy` to be installed.'
            ) from e
        return np.vectorize(OperationCounter.wrap, otypes=[object])(a)
    
    
    @overload
    @staticmethod
    def unwrap(x:OperationCounter[T]) -> T: ...
    @overload
    @staticmethod
    def unwrap(x:T) -> T: ...
    @staticmethod
    def unwrap(x:Any) -> Any:
        """Extract the underlying value if `x` is an `OperationCounter`."""
        return x.v if isinstance(x, OperationCounter) else x
    
    @staticmethod
    def unwrapCollection(s:Collection[OperationCounter[T]]) -> Collection[T]:
        """Unwrap the elements of `s` from `OperationCounter`s."""
        if isinstance(s, Mapping):
            return type(s)(
                    (OperationCounter.unwrap(k), OperationCounter.unwrap(v))
                    for k, v in s.items())
        elif isinstance(s, (Set, Sequence)):
            return type(s)(map(OperationCounter.unwrap, s))
        else:
            raise TypeError(f'Unsupported type: {type(s)}')
    
    @staticmethod
    def unwrapArray(a:Any) -> Any:
        """Return `np.ndarray(a)` with all elements unwrapped."""
        try:
            import numpy as np
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                'OperationCounter.unwrapArray requires `numpy` to be installed.'
            ) from e
        return np.vectorize(OperationCounter.unwrap, otypes=[object])(a)
    
    
    @staticmethod
    def grouped(counter:Counter[str]) -> Counter[str]:
        """Group individual operation counts into broader categories.
        
        Counts are summed into the following groups:
        
        - Comparisons
            - `cmp`      = `lt` + `le` + `eq` + `ne` + `gt` + `ge`
        - Unary operations are left as they are
            - `pos`, `neg`, `abs`, `invert`
        - Arithmetic
            - `add`      = `add` + `iadd` + `radd`
            - `sub`      = `sub` + `isub` + `rsub`
            - `mul`      = `mul` + `imul` + `rmul`
            - `truediv`  = `truediv` + `itruediv` + `rtruediv`
            - `floordiv` = `floordiv` + `ifloordiv` + `rfloordiv`
            - `mod`      = `mod` + `imod` + `rmod`
            - `pow`      = `pow` + `ipow` + `rpow`
            - `divmod`   = `divmod` + `rdivmod`
        - Bitwise
            - `and`      = `and` + `iand` + `rand`
            - `or`       = `or` + `ior` + `ror`
            - `xor`      = `xor` + `ixor` + `rxor`
            - `lshift`   = `lshift` + `ilshift` + `rlshift`
            - `rshift`   = `rshift` + `irshift` + `rrshift`
        
        Unrecognised counts are copied unchanged.
        
        Parameters
        ----------
        counter: Counter[str]
            A mapping from operation names to the number of times each
            operation has been executed.
        
        Returns
        -------
        Counter[str]
            A new counter where related operations are summed together under
            a single key.
        """
        families:dict[str, tuple[str, ...]] = {
            #comparison
            'cmp':      ('lt', 'le', 'eq', 'ne', 'gt', 'ge'),
            #unary
            'pos':      ('pos',),
            'neg':      ('neg',),
            'abs':      ('abs',),
            'invert':   ('invert',),
            #arithmetic
            'add':      ('add', 'iadd', 'radd'),
            'sub':      ('sub', 'isub', 'rsub'),
            'mul':      ('mul', 'imul', 'rmul'),
            'truediv':  ('truediv', 'itruediv', 'rtruediv'),
            'floordiv': ('floordiv', 'ifloordiv', 'rfloordiv'),
            'mod':      ('mod', 'imod', 'rmod'),
            'pow':      ('pow', 'ipow', 'rpow'),
            'divmod':   ('divmod', 'rdivmod'),
            #bitwise
            'and':      ('and', 'iand', 'rand'),
            'or':       ('or', 'ior', 'ror'),
            'xor':      ('xor', 'ixor', 'rxor'),
            'lshift':   ('lshift', 'ilshift', 'rlshift'),
            'rshift':   ('rshift', 'irshift', 'rrshift')
        }
        
        grouped:Counter[str] = Counter()
        for family, keys in families.items():
            if (s := sum(counter.get(k, 0) for k in keys)):
                grouped[family] = s
        
        #keep any keys we didn't map
        mapped_keys = {k for keys in families.values() for k in keys}
        for k, v in counter.items():
            if k not in mapped_keys:
                grouped[k] += v
        
        return grouped
    
    
    
    # --- output ---
    def __repr__(self) -> str:
        return f'OperationCounter({self.v!r})'
    
    def __str__(self) -> str:
        return f'OperationCounter({self.v})'
    
    def __format__(self, spec:str) -> str:
        return format(self.v, spec)
    
    def __hash__(self) -> int:
        return hash(self.v)
    
    
    # --- special arithmetic (non-regular signatures) ---
    def __pow__(self, other:Any, mod:Optional[int]=None) \
            -> OperationCounter[T]:
        OperationCounter.counter['pow'] += 1
        o = OperationCounter.unwrap(other)
        return OperationCounter(
                pow(self.v, o, mod) if mod is not None else pow(self.v, o))
    
    def __rpow__(self, other:Any, mod:Optional[int]=None) \
            -> OperationCounter[T]:
        OperationCounter.counter['rpow'] += 1
        o = OperationCounter.unwrap(other)
        return OperationCounter(
                pow(o, self.v, mod) if mod is not None else pow(o, self.v))
    
    def __ipow__(self, other:Any, mod:Optional[int]=None) \
            -> OperationCounter[T]:
        OperationCounter.counter['ipow'] += 1
        o = OperationCounter.unwrap(other)
        self.v = pow(self.v, o, mod) if mod is not None else pow(self.v, o)
        return self
    
    def __divmod__(self, other:Any) \
            -> tuple[OperationCounter[T], OperationCounter[T]]:
        OperationCounter.counter['divmod'] += 1
        q, r = divmod(self.v, OperationCounter.unwrap(other))
        return OperationCounter(q), OperationCounter(r)
    
    def __rdivmod__(self, other:Any) \
            -> tuple[OperationCounter[T], OperationCounter[T]]:
        OperationCounter.counter['rdivmod'] += 1
        q, r = divmod(OperationCounter.unwrap(other), self.v)
        return OperationCounter(q), OperationCounter(r)



# --- operation factories ---
def _convert(key, fn):
    def method(self):
        OperationCounter.counter[key] += 1
        return fn(self.v)
    return method

for _name, _fn in {'bool':    bool,
                   'int':     int,
                   'float':   float,
                   'complex': complex}.items():
    setattr(OperationCounter, f'__{_name}__', _convert(_name, _fn))


def _cmp(key, fn):
    def method(self, other):
        OperationCounter.counter[key] += 1
        return fn(self.v, OperationCounter.unwrap(other))
    return method

for _name, _fn in {'lt': operator.lt,
                   'le': operator.le,
                   'eq': operator.eq,
                   'ne': operator.ne,
                   'gt': operator.gt,
                   'ge': operator.ge}.items():
    setattr(OperationCounter, f'__{_name}__', _cmp(_name, _fn))


def _unary(key, fn):
    def method(self):
        OperationCounter.counter[key] += 1
        return OperationCounter(fn(self.v))
    return method

for _name, _fn in {'pos':    operator.pos,
                   'neg':    operator.neg,
                   'abs':    abs,
                   'invert': operator.invert}.items():
    setattr(OperationCounter, f'__{_name}__', _unary(_name, _fn))


def _binary(key, fn):
    def method(self, other):
        OperationCounter.counter[key] += 1
        return OperationCounter(fn(self.v, OperationCounter.unwrap(other)))
    return method

def _rbinary(key, fn):
    def method(self, other):
        OperationCounter.counter[key] += 1
        return OperationCounter(fn(OperationCounter.unwrap(other), self.v))
    return method

def _ibinary(key, fn):
    def method(self, other):
        OperationCounter.counter[key] += 1
        self.v = fn(self.v, OperationCounter.unwrap(other))
        return self
    return method

for _name, (_fn, _ifn) in {
        'add':      (operator.add,      operator.iadd),
        'sub':      (operator.sub,      operator.isub),
        'mul':      (operator.mul,      operator.imul),
        'matmul':   (operator.matmul,   operator.imatmul),
        'truediv':  (operator.truediv,  operator.itruediv),
        'floordiv': (operator.floordiv, operator.ifloordiv),
        'mod':      (operator.mod,      operator.imod),
        'and':      (operator.and_,     operator.iand),
        'or':       (operator.or_,      operator.ior),
        'xor':      (operator.xor,      operator.ixor),
        'lshift':   (operator.lshift,   operator.ilshift),
        'rshift':   (operator.rshift,   operator.irshift)}.items():
    setattr(OperationCounter, f'__{_name}__',  _binary(_name, _fn))
    setattr(OperationCounter, f'__r{_name}__', _rbinary(f'r{_name}', _fn))
    setattr(OperationCounter, f'__i{_name}__', _ibinary(f'i{_name}', _ifn))
#pow, rpow, ipow, divmod, rdivmod don't fit this pattern
#and are therefore written explicitly



@contextmanager
def count_ops() -> Generator[Counter[str]]:
    """Context manager that yields the operation counter.
    
    The `OperationCounter.counter` is cleared on entry and yielded to the
    caller.
    
    Yields
    ------
    Counter[str]
        The global `OperationCounter.counter`.
    """
    OperationCounter.reset()
    yield OperationCounter.counter
