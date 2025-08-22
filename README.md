# OperationCounter

**OperationCounter** is a lightweight Python utility class for
**tracking arithmetic and comparison operations**. It is designed to perform
complexity analysis empirically and exactly.

Unlike profilers (which measure *time*), OperationCounter counts *operations*
like `add`, `iadd`, `lt`, `pow`, `divmod`, etc., giving you a cost model that
is independent of machine speed.

## Installation

```bash
git clone https://github.com/goessl/operationcounter.git
```

## Features

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

## Why not just use a profiler?

Profilers measure wall-clock time or CPU usage, which depends on machine,
libraries, and optimizations resulting in machine dependent and noisy results.
**OperationCounter** instead counts *abstract operations* — closer to what we
use in algorithm analysis (e.g. “merge sort does O(n log n) comparisons”).

I also enable **exact counting**, so that not just a big-O result like
$\mathcal{O}(n^2)$ can be given but rather "this function does $n^2+3n+2$
multiplications and $4n+1$ additions".

## Usage

```python
>>> from operationcounter import OperationCounter, count_ops
>>> a = OperationCounter(3)
>>> b = OperationCounter(5)
>>> c = a * b + 2
>>> if c > 10:
...     c -= 1
... OperationCounter.counter
Counter({'mul': 1, 'add': 1, 'gt': 1, 'isub': 1})
```
Or more sophisticated to verify that [iterative polynomial
evaluation](https://en.wikipedia.org/wiki/Horner%27s_method#Efficiency) takes
$n$ additions and $2n-1$ multiplications.
```python
>>> from itertools import accumulate, repeat
>>> from functools import reduce
>>> from operator import mul
>>> 
>>> def polyval_iterative(p, x):
...     """Return the polynomial `p` evaluated at point `x`.
...     
...     Uses iterative monomial calculation.
...     """
...     #don't do
...     #return sumprod(p, accumulate(repeat(x, len(p)-1), mul, initial=type(x)(1)))
...     #as it would introduce two unnecessary multiplications
...     # one in accumulate: 1, 1*x, x*x, x^2*x, ...
...     # and one in the sumprod: p[0]*1 + p[1]*x + [p2]*x^2 + ...
...     monomials = (type(x)(1),) + tuple(accumulate(repeat(x, len(p)-1), mul))
...     return sum(map(mul, p[1:], monomials[1:]), p[0])
...     
>>> p = [1, 2, 3] #polynomial of degree n=2
>>> x = 5
>>> 
>>> from operationcounter import OperationCounter, count_ops
>>> 
>>> p = tuple(map(OperationCounter, p))
>>> x = OperationCounter(x)
>>> 
>>> with count_ops() as counter:
...     assert polyval_iterative(p, x) == 86
... OperationCounter.counter
... 
Counter({'mul': 3, 'add': 2, 'eq': 1})
```

### Class: `OperationCounter[T]`

Wrap a value and count the operations performed on it. All arithmetic, bitwise,
and comparison operations are intercepted and counted.
  
#### Attributes

- `counter: Counter[str]`
  Live global counter of all operations.

#### Static methods

- `reset() -> None`
  Clear all recorded operation counts.

- `snapshot() -> Counter[str]`
  Return a copy of the current operation counts.

- `unwrap(x: OperationCounter[T] | T) -> T`
  Extract the underlying value if `x` is an `OperationCounter`.

- `grouped(counter: Counter[str]) -> Counter[str]`
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

### Context manager: `count_ops()`

Context manager that yields the operation counter. The
`OperationCounter.counter` is cleared on entry and yielded to the caller.
```python
with count_ops() as counts:
    # run algorithm with `OperationCounter`-wrapped inputs
    ...
print(counts)
```

### Functions: `reduce_default`, `sum_default`, `prod_default` & `sumprod_default`

- `reduce_default(function, iterable, default=0)`: Apply function of two
  arguments cumulatively to the items of iterable.
  
  Like `functools.reduce` but without the function applied to some initial
  element and the first element in the iterable. Returns `default` if
  `iterable` is empty.
- `sum_default(iterable, default=0)`: Return the sum of all elements in
  iterable.
  
  Like `sum` but without the default initial `0+`. Returns `default` if
  `iterable` is empty.
- `prod_default(iterable, default=1)`: Return the product of all elements in
  iterable.
  
  Like `math.prod` but without the default initial `1*`. Returns `default` if
  `iterable` is empty.
- `sumprod_default(a, b, default=0)`: Return the sum-product of all elements in
  the iterables.
  
  Like `math.sumprod` but without the default initial `0+`. Returns `default`
  if any iterable is empty. Zips both iterables, so they can be of different
  length.

## Warning

Special attention has to be payed to built-in functions like
[`sum`](https://docs.python.org/3/library/functions.html#sum). It prepends an
initial `+int(0)` (to correctly return the neutral element for an empty sum)
and therefore increments the addition counter too.

For such applications use the provided `reduce_default`, `sum_default`,
`prod_default` & `sumprod_default`.

## Limitations

- Only counts operations performed **through the wrapper**.
  If your algorithm manipulates raw `int` or `float`, those ops are invisible.
- Does not catch operations executed inside C extensions (e.g. NumPy vectorized
  ops).
- Uses a **global counter**; multi-threaded code may need thread-local storage
  (planned feature).

## Roadmap

- [x] `sum`, `sumprod`(?), `reduce` with default instead of initial argument
- [ ] Log all operations with operands so that the binary complexity can be
  determined.
- [ ] Threading
- [ ] More flexible grouping schemes (choose your own families)
- [ ] Helper to wrap elements of sequences or `numpy.array`s.

## License (MIT)

Copyright (c) 2025 Sebastian Gössl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
