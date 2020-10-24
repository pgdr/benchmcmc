# benchmcmc — Benchmark analysis with MCMC

## Install

Installing is as always

```
pip install benchmcmc
```

It depends on [`pymc3`](https://pypi.org/project/pymc3/) and
[`matplotlib`](https://pypi.org/project/matplotlib/), so these are also
installed.

## Quickstart

Getting started real quick:

```
benchmcmc --generate 69 11 10 131 10 9 --beta > bench.txt
benchmcmc bench.txt
```


## Introduction

This package lets you take a series of benchmark data analyses whether
there at one point was a change in performance.

Suppose that you run your benchmark tests on every commit that you have
(e.g. using `git-filter-branch`), and you see that your performance data
is, e.g. in requests per second or in seconds, or other measures.  (In
this data, it starts being centered around 13+ε or so, and it ends being
centered around 12+ε or so.)

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

There seems to be a slight drop in values before the 100th point, but
it's not easy to determine exactly where the change occurred.

Suppose that you wonder whether or not the performance at the start and
at the end are likely to be from two different distributions, and if so,
where the _switchpoint_ was.

![traceplot](https://raw.githubusercontent.com/pgdr/benchmcmc/main/assets/benchmcmc.png)

## Analysis

Running `benchmcmc` on the data gives the above plot which shows that it
is likely that the performance went from ~13.5 to 12.25 at or around the
69th or 75th datapoints.

This helps you pin down when a performance change might have occurred.


---

## Generating synthetic data

You can run `benchmcmc --generate` for generating synthetic benchmark
data.

```bash
$ python mkbench.py 100 15 3 100 14 3 [--beta] > benchmarkfile.txt
```

This generates 200 samples, 100 from `N(mu=15, sigma=3)` followed by 100
from `N(mu=14, sigma=3)`.

If you use `--beta`, you get a bit more realistic performance with a
_lower bound_ of mu.
