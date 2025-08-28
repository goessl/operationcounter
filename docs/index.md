# operationcounter

**operationcounter** is a Python package for
**tracking arithmetic and comparison operations**. It is designed to perform
complexity analysis empirically and exactly.

Unlike profilers (which measure *time*), `OperationCounter` counts *operations*
like `add`, `iadd`, `lt`, `pow`, `divmod`, etc., giving you a cost model that
is independent of machine speed.

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

## Installation

```bash
git clone https://github.com/goessl/operationcounter.git
```

## Features

- **A class `OperationCounter`** that wraps any Python value and tracks:
    - Arithmetic operations: `+`, `-`, `*`, `/`, `//`, `%`, `**`, `divmod`
    - Bitwise operations: `&`, `|`, `^`, `<<`, `>>`
    - Unary operations: `+x`, `-x`, `abs(x)`, `~x`
    - Comparisons: `<`, `<=`, `==`, `!=`, `>`, `>=`
- **Exact accumulators** that don't perform any unnecessary operations like `+0` or
  `*1` and allow for an **initial and a default argument**:
    - `reduce_default`,
    - `sum_default`,
    - `prod_default` &
    - `sumprod_default`.

## Why not just use a profiler?

Profilers measure wall-clock time or CPU usage, which depends on machine,
libraries, and optimizations resulting in machine dependent and noisy results.
`OperationCounter` instead counts *abstract operations separately* - closer to what we
use in algorithm analysis (e.g. "merge sort does $\mathcal{O}(n\log n)$ comparisons").

It also enables *exact counting*, so that not just a big-O result like
$\mathcal{O}(n^2)$ can be given but rather "this function does $n^2+3n+2$
multiplications and $4n+1$ additions".

## Demonstration

To verify that [iterative polynomial
evaluation](https://en.wikipedia.org/wiki/Horner%27s_method#Efficiency) takes
$n$ additions and $2n-1$ multiplications.
```python
>>> from itertools import accumulate, repeat
>>> from functools import reduce
>>> from operator import mul
>>> from operationcounter import OperationCounter, count_ops, sumprod_default
>>> 
>>> def polyval_iterative(p, x):
...     """Return the polynomial `p` evaluated at point `x`.
...     
...     Uses iterative monomial calculation.
...     """
...     #don't do
...     #return sumprod(p, accumulate(repeat(x, len(p)-1), mul, initial=type(x)(1)))
...     #as it would introduce two unnecessary multiplications and one addition:
...     # one multiplication in accumulate: 1, 1*x, x*x, x^2*x, ...,
...     # another one in sumprod: p[0]*1 + p[1]*x + p[2]*x^2 + ...
...     # and an addition in sumprod: 0 + p[0] + p[1]x + ...
...     monomials = (type(x)(1),) + tuple(accumulate(repeat(x, len(p)-1), mul))
...     return sumprod_default(p[1:], monomials[1:], initial=p[0])
...     
>>> p = [1, 2, 3] # 1+2x+3x^2
>>> x = 5
>>> 
>>> p = tuple(map(OperationCounter, p))
>>> x = OperationCounter(x)
>>> 
>>> with count_ops() as counts:
...     assert polyval_iterative(p, x) == 86
...     counts
...     
Counter({'mul': 3, 'add': 2, 'eq': 1})
```

## Warning

Special attention has to be paid to built-in functions like
[`sum`](https://docs.python.org/3/library/functions.html#sum). It prepends an
initial `+int(0)` (to correctly return the neutral element for an empty sum)
and therefore increments the addition counter too.

For such applications **use the provided `reduce_default`, `sum_default`,
`prod_default` & `sumprod_default`**.

## Limitations

- **Only counts operations performed through the wrapper**.
  If your algorithm manipulates raw `int` or `float`, those ops are invisible.
- Does not catch operations executed inside C extensions (e.g. `numpy.linalg`).
- Uses a global counter; multi-threaded code may need thread-local storage
  (planned feature).

## Roadmap

- [x] `reduce`, `sum`, `prod` & `sumprod` with default argument.
- [ ] Accumulators as C extension.
- [ ] Log all operations with operands so that the binary complexity can be
  determined.
- [ ] Threading.
- [ ] More flexible grouping schemes (choose your own families).
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
