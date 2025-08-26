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
- `reduce_default`, `sum_default`, `prod_default` & `sumprod_default` that
  don't perform any unnecessary operations like `+0` or `*1`.
"""

from .operationcounter import *
from .accumulators import *
