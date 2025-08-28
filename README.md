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

Read the [documentation webpage](https://goessl.github.io/operationcounter)
or read the [raw markdown](docs/index.md).

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
