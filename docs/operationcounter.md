# OperationCounter & count_ops

## Class: `OperationCounter[T]`

Wrap a value and count the operations performed on it. All arithmetic, bitwise,
and comparison operations are intercepted and counted.
  
### Attributes

- `counter: Counter[str]`:
    
    Live global counter of all operations.

### Static methods

- `reset() -> None`:
    
    Clear all recorded operation counts.

- `snapshot() -> Counter[str]`:
    
    Return a copy of the current operation counts.

- `unwrap(x: OperationCounter[T] | T) -> T`:
    
    Extract the underlying value if `x` is an `OperationCounter`.

- `grouped(counter: Counter[str]) -> Counter[str]`:
    
    Group individual operation counts into broader categories.
    
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
    
    `counter`: Counter[str]
    
    A mapping from operation names to the number of times each operation has
    been executed.
    
    Returns
    
    `Counter[str]`
    
    A new counter where related operations are summed together under a single
    key.

## Context manager: `count_ops()`

Context manager that yields the operation counter. The
`OperationCounter.counter` is cleared on entry and yielded to the caller.
```python
with count_ops() as counts:
    # run algorithm with `OperationCounter`-wrapped inputs
    ...
    print(counts)
```
