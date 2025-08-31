# Accumulators

``` mermaid
graph TD
  Z(["<code>sum(iterable, initial=initial, default=default)</code>"]) --> A{"<code>initial</code> <code>MISSING</code>?"};
  A --> |no| B["<code>return initial+...</code>"];
  A --> |yes| C{"<code>iterable</code> empty?"};
  C --> |no| D["<code>return iterable[0]+...</code>"];
  C --> |yes| E{"<code>default</code> <code>MISSING</code>?"};
  E --> |no| F["<code>return default</code>"];
  E --> |yes| G["<code>raise TypeError</code>"];
```

::: operationcounter.accumulators
