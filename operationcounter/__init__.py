"""operationcounter package.

**operationcounter** is a Python package for
**tracking arithmetic and comparison operations**. It is designed to perform
complexity analysis empirically and exactly.

Unlike profilers (which measure *time*), `OperationCounter` counts *operations*
like `add`, `iadd`, `lt`, `pow`, `divmod`, etc., giving you a cost model that
is independent of machine speed.
"""



from .operationcounter import *
from .accumulators import *
from .iterators import *
