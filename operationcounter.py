"""Utilities for counting Python operations.

**OperationCounter** is a lightweight Python utility class for
**tracking arithmetic and comparison operations**. It is designed to perform
complexity analysis empirically and exactly.

Unlike profilers (which measure *time*), OperationCounter counts *operations*
like `add`, `iadd`, `lt`, `pow`, `divmod`, etc., giving you a cost model that
is independent of machine speed.

- Wraps any Python value and tracks:
  - **Arithmetic operations**: `+`, `-`, `*`, `/`, `//`, `%`, `**`, `divmod`
  - **Bitwise operations**: `&`, `|`, `^`, `<<`, `>>`
  - **Unary operations**: `+x`, `-x`, `abs(x)`, `~x`
  - **Comparisons**: `<`, `<=`, `==`, `!=`, `>`, `>=`
- Distinguishes **static**, **reversed**, and **in-place** operations  
  (`add` vs `radd` vs `iadd`) so that different algorithm implementations can
  be accounted separately.
- Provides a `grouped` view to collapse operation families for easier reporting.
- Simple `count_ops()` context manager for clean measurement runs.
"""

from __future__ import annotations
from collections import Counter
from contextlib import contextmanager
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar, overload

T = TypeVar('T')



class OperationCounter(Generic[T]):
    """Wrap a value and count the operations performed on it.
    
    All arithmetic, bitwise, and comparison operations are intercepted and
    counted.
    """
    
    
    counter: Counter[str] = Counter()
    """Live global counter of all operations."""
    
    def __init__(self, v: T) -> None:
        """Wrap `v` into an `OperationCounter`."""
        self.v: T = v
    
    
    # --- utilities ---
    @staticmethod
    def reset() -> None:
        """Clear all recorded operation counts."""
        OperationCounter.counter.clear()
    
    @staticmethod
    def snapshot() -> Counter[str]:
        """Return a copy of the current operation counts."""
        return OperationCounter.counter.copy()
    
    @overload
    @staticmethod
    def unwrap(x: OperationCounter[T]) -> T: ...
    @overload
    @staticmethod
    def unwrap(x: T) -> T: ...
    @staticmethod
    def unwrap(x: Any) -> Any:
        """Extract the underlying value if `x` is an `OperationCounter`."""
        return x.v if isinstance(x, OperationCounter) else x
    
    @staticmethod
    def grouped(counter: Counter[str]) -> Counter[str]:
        """Group individual operation counts into broader categories.
        
        Counts are summed into the following groups:
        Comparisons
        - `cmp`      = `lt` + `le` + `eq` + `ne` + `gt` + `ge`
        Unary operations are left as they are
        - `pos`, `neg`, `abs`, `invert`
        Arithmetic
        - `add`      = `add` + `iadd` + `radd`
        - `sub`      = `sub` + `isub` + `rsub`
        - `mul`      = `mul` + `imul` + `rmul`
        - `truediv`  = `truediv` + `itruediv` + `rtruediv`
        - `floordiv` = `floordiv` + `ifloordiv` + `rfloordiv`
        - `mod`      = `mod` + `imod` + `rmod`
        - `pow`      = `pow` + `ipow` + `rpow`
        - `divmod`   = `divmod` + `rdivmod`
        Bitwise
        - `and`      = `and` + `iand` + `rand`
        - `or`       = `or` + `ior` + `ror`
        - `xor`      = `xor` + `ixor` + `rxor`
        - `lshift`   = `lshift` + `ilshift` + `rlshift`
        - `rshift`   = `rshift` + `irshift` + `rrshift`
        
        Unrecognised counts are copied unchanged.
        
        Parameters
        ----------
        counter:
            A mapping from operation names to the number of times each
            operation has been executed.
        
        Returns
        -------
        Counter[str]
            A new counter where related operations are summed together under
            a single key.
        """
        families: Dict[str, Tuple[str]] = {
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
        
        grouped: Counter[str] = Counter()
        for family, keys in families.items():
            grouped[family] = sum(counter.get(k, 0) for k in keys)
        
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
    
    def __format__(self, spec: str) -> str:
        return format(self.v, spec)
    
    
    # --- conversion ---
    def __bool__(self) -> bool:
        OperationCounter.counter['bool'] += 1
        return bool(self.v)
    
    def __int__(self) -> int:
        OperationCounter.counter['int'] += 1
        return int(self.v)
    
    def __float__(self) -> float:
        OperationCounter.counter['float'] += 1
        return float(self.v)
    
    def __complex__(self) -> complex:
        OperationCounter.counter['complex'] += 1
        return complex(self.v)
    
    
    # --- comparison ---
    def __lt__(self, other: Any) -> bool:
        OperationCounter.counter['lt'] += 1
        return self.v < OperationCounter.unwrap(other)
    
    def __le__(self, other: Any) -> bool:
        OperationCounter.counter['le'] += 1
        return self.v <= OperationCounter.unwrap(other)
    
    def __eq__(self, other: Any) -> bool:
        OperationCounter.counter['eq'] += 1
        return self.v == OperationCounter.unwrap(other)
    
    def __ne__(self, other: Any) -> bool:
        OperationCounter.counter['ne'] += 1
        return self.v != OperationCounter.unwrap(other)
    
    def __gt__(self, other: Any) -> bool:
        OperationCounter.counter['gt'] += 1
        return self.v > OperationCounter.unwrap(other)
    
    def __ge__(self, other: Any) -> bool:
        OperationCounter.counter['ge'] += 1
        return self.v >= OperationCounter.unwrap(other)
    
    
    # --- unary ---
    def __pos__(self) -> OperationCounter[T]:
        OperationCounter.counter['pos'] += 1
        return OperationCounter(+self.v)
    
    def __neg__(self) -> OperationCounter[T]:
        OperationCounter.counter['neg'] += 1
        return OperationCounter(-self.v)
    
    def __abs__(self) -> OperationCounter[T]:
        OperationCounter.counter['abs'] += 1
        return OperationCounter(abs(self.v))
    
    def __invert__(self) -> OperationCounter[T]:
        OperationCounter.counter['invert'] += 1
        return OperationCounter(~self.v)
    
    
    # --- arithmetic ---
    def __add__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['add'] += 1
        return OperationCounter(self.v + OperationCounter.unwrap(other))
    
    def __radd__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['radd'] += 1
        return OperationCounter(OperationCounter.unwrap(other) + self.v)
    
    def __iadd__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['iadd'] += 1
        self.v = self.v + OperationCounter.unwrap(other)
        return self
    
    
    def __sub__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['sub'] += 1
        return OperationCounter(self.v - OperationCounter.unwrap(other))
    
    def __rsub__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rsub'] += 1
        return OperationCounter(OperationCounter.unwrap(other) - self.v)
    
    def __isub__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['isub'] += 1
        self.v = self.v - OperationCounter.unwrap(other)
        return self
    
    
    def __mul__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['mul'] += 1
        return OperationCounter(self.v * OperationCounter.unwrap(other))
    
    def __rmul__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rmul'] += 1
        return OperationCounter(OperationCounter.unwrap(other) * self.v)
    
    def __imul__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['imul'] += 1
        self.v = self.v * OperationCounter.unwrap(other)
        return self
    
    
    def __truediv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['truediv'] += 1
        return OperationCounter(self.v / OperationCounter.unwrap(other))
    
    def __rtruediv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rtruediv'] += 1
        return OperationCounter(OperationCounter.unwrap(other) / self.v)
    
    def __itruediv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['itruediv'] += 1
        self.v = self.v / OperationCounter.unwrap(other)
        return self
    
    
    def __floordiv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['floordiv'] += 1
        return OperationCounter(self.v // OperationCounter.unwrap(other))
    
    def __rfloordiv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rfloordiv'] += 1
        return OperationCounter(OperationCounter.unwrap(other) // self.v)
    
    def __ifloordiv__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ifloordiv'] += 1
        self.v = self.v // OperationCounter.unwrap(other)
        return self
    
    
    def __mod__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['mod'] += 1
        return OperationCounter(self.v % OperationCounter.unwrap(other))
    
    def __rmod__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rmod'] += 1
        return OperationCounter(OperationCounter.unwrap(other) % self.v)
    
    def __imod__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['imod'] += 1
        self.v = self.v % OperationCounter.unwrap(other)
        return self
    
    
    def __pow__(self, other: Any, mod: Optional[int] = None) \
            -> OperationCounter[T]:
        OperationCounter.counter['pow'] += 1
        o = OperationCounter.unwrap(other)
        return OperationCounter(
                pow(self.v, o, mod) if mod is not None else pow(self.v, o))
    
    def __rpow__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rpow'] += 1
        return OperationCounter(pow(OperationCounter.unwrap(other), self.v))
    
    def __ipow__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ipow'] += 1
        self.v = pow(self.v, OperationCounter.unwrap(other))
        return self
    
    
    def __divmod__(self, other: Any) \
            -> Tuple[OperationCounter[T], OperationCounter[T]]:
        OperationCounter.counter['divmod'] += 1
        q, r = divmod(self.v, OperationCounter.unwrap(other))
        return OperationCounter(q), OperationCounter(r)
    
    def __rdivmod__(self, other: Any) \
            -> Tuple[OperationCounter[T], OperationCounter[T]]:
        OperationCounter.counter['rdivmod'] += 1
        q, r = divmod(OperationCounter.unwrap(other), self.v)
        return OperationCounter(q), OperationCounter(r)
    
    
    # --- bitwise ---
    def __and__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['and'] += 1
        return OperationCounter(self.v & OperationCounter.unwrap(other))
    
    def __rand__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rand'] += 1
        return OperationCounter(OperationCounter.unwrap(other) & self.v)
    
    def __iand__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['iand'] += 1
        self.v = self.v & OperationCounter.unwrap(other)
        return self
    
    
    def __or__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['or'] += 1
        return OperationCounter(self.v | OperationCounter.unwrap(other))
    
    def __ror__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ror'] += 1
        return OperationCounter(OperationCounter.unwrap(other) | self.v)
    
    def __ior__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ior'] += 1
        self.v = self.v | OperationCounter.unwrap(other)
        return self
    
    
    def __xor__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['xor'] += 1
        return OperationCounter(self.v ^ OperationCounter.unwrap(other))
    
    def __rxor__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rxor'] += 1
        return OperationCounter(OperationCounter.unwrap(other) ^ self.v)
    
    def __ixor__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ixor'] += 1
        self.v = self.v ^ OperationCounter.unwrap(other)
        return self
    
    
    def __lshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['lshift'] += 1
        return OperationCounter(self.v << OperationCounter.unwrap(other))
    
    def __rlshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rlshift'] += 1
        return OperationCounter(OperationCounter.unwrap(other) << self.v)
    
    def __ilshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['ilshift'] += 1
        self.v = self.v << OperationCounter.unwrap(other)
        return self
    
    
    def __rshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rshift'] += 1
        return OperationCounter(self.v >> OperationCounter.unwrap(other))
    
    def __rrshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['rrshift'] += 1
        return OperationCounter(OperationCounter.unwrap(other) >> self.v)
    
    def __irshift__(self, other: Any) -> OperationCounter[T]:
        OperationCounter.counter['irshift'] += 1
        self.v = self.v >> OperationCounter.unwrap(other)
        return self



@contextmanager
def count_ops():
    """Context manager that yields the operation counter.
    
    The `OperationCounter.counter` is cleared on entry and yielded to the
    caller.
    """
    OperationCounter.reset()
    try:
        yield OperationCounter.counter
    finally:
        pass
