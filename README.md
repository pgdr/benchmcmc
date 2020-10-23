# benchmcmc — Benchmark analysis with MCMC

This script lets you take a series of benchmark data and see if at one
point there was a change performance.

Suppose that you run your benchmark tests on every commit that you have
(e.g. using `git-filter-branch`), and you see that your performance data
is, e.g. in requests per second or in seconds, or other measures

```
13.64
12.82
11.69
15.12
12.30
18.46
13.51
14.33
13.84
12.77
... (180 rows omitted)
10.93
11.02
12.45
11.78
12.12
13.51
10.66
10.18
10.81
12.19
```

(or visualized)

![scatterplot of performance over time](https://raw.githubusercontent.com/pgdr/benchmcmc/main/assets/benchscatter.png)

Suppose that you wonder whether or not the performance at the start and
at the end are likely to be from two different distributions, and if so,
where the _switchpoint_ was.

Running MCMC on the data gives this plot which shows that it is likely
that the performance went from ~13.5 to 12.25 at or around the 69th
datapoint.

![traceplot](https://raw.githubusercontent.com/pgdr/benchmcmc/main/assets/benchmcmc.png)
