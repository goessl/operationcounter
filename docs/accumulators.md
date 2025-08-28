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

## Missing

`MISSING`

Sentinel to mark empty parameters.

## reduce

`reduce_default(function, iterable, *, initial=MISSING, default=0)`

Apply function of two arguments cumulatively to the iterable.

Like `functools.reduce` but with an optional initial element and an optional
default return value.
Difference to `functools.reduce`:

- If `iterable` is empty and `initial` and `default` is `MISSING`, an
  `TypeError` is raised.
- If `iterable` is empty and `initial` is `MISSING`, but `default` is not, then
  `default` is returned.

## sum

`def sum_default(iterable, *, initial=MISSING, default=0)`

Return the sum of all elements in the iterable.

Like `sum` but with an optional initial element and an optional default return
value.

- If `iterable` is empty and `initial` and `default` is `MISSING`, an
  `TypeError` is raised.
- If `iterable` is empty and `initial` is `MISSING`, but `default` is not, then
  `default` is returned.
- If `initial` is `MISSING`, then there is truly no initial `0 +=`.

## prod

`prod_default(iterable, *, initial=MISSING, default=1)`

Return the product of all elements in the iterable.

Like `math.prod` but with an optional initial element and an optional default
return value.

- If `iterable` is empty and `initial` and `default` is `MISSING`, an
  `TypeError` is raised.
- If `iterable` is empty and `initial` is `MISSING`, but `default` is not,
  then `default` is returned.
- If `initial` is `MISSING`, then there is truly no initial `1 *=`.

## sumprod

`sumprod_default(a, b, *, initial=MISSING, default=0)`

Return the sum-product of all elements in the iterables.

Like `math.sumprod` but with an optional initial element, an optional default
return value and non-strict zipping of both iterables.

- If `a` or `b` is empty and `initial` and `default` is `MISSING`, an
  `TypeError` is raised.
- If `a` or `b` is empty and `initial` is `MISSING`, but `default` is not,
  then `default` is returned.
- If `initial` is `MISSING`, then there is truly no initial `0 +=`.

## default

[No, `default` isn't a Python keyword.](https://docs.python.org/3/reference/lexical_analysis.html#keywords)
