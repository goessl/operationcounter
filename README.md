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

## Documentation

**Enjoy the [documentation webpage](https://goessl.github.io/operationcounter).**

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

## Roadmap

- [x] `reduce`, `sum`, `prod` & `sumprod` with default argument.
- [x] Wrap collections.
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
