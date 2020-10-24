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
(e.g. looping over `git-rev-list`),
and you see that your performance data
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


## Running a script on a history

Suppose that you want to run `python script.py` on a script that is in
your Git tree.

```bash
LOGFILE=/tmp/timescript
echo "" > $LOGFILE
for commit in $(git rev-list master)
do
    git checkout $commit
    git log | head -n 1 >> $LOGFILE
    /usr/bin/time -a -o $LOGFILE --format=%e python script.py
done
tac $LOGFILE
```

Running with a test-repo, it outputs something like this:

```
commit e1f5f9f904e45f93aad31400a1d7dd335aff99a9
0.10
commit 80027744d2fd3809daeaabded1fb2a8e2bbbe601
0.09
commit 504cf733151c692ceeb0e403087f341279afe750
0.08
commit b45671449b3a7e3345e4840f5e78ca076c9b3c39
0.07
commit 9136914345a4574af5c257de86aba4eb020efa9f
0.07
commit a32ce81dccef6b2a14cddc97496dff30cd2d1b7c
0.07
commit b3ba887e134b001b2f7445f38fb67cb036edbf8a
0.07
commit ec7f042e8c8fc9e703b18e480af85b078cbc6806
0.07
commit 6cc7cdd3f35896555e74c61a9d4f7c5aa4cd1ad8
0.07
commit 065b6a55a0e6a5d1f884a1d1acaef755799a9261
0.07
commit 7a9c111ec707b76349068dbe6f3f73ed5b68e6d5
0.07
commit b22278d60919e0570adf16a67f392d7d2abfbd83
0.07
commit 9c08050aa6b780e570ef4cc164bfda3f2ef77669
0.07
commit 4c56a54154e1f00d04baf748bafa90a735b53f76
0.04
commit b34b1469dc5a0dea671fcbdf94f7b9318d53c59d
0.04
commit 43db50cb72c2944e100b3ec413ea3e1119c25dd0
0.04
commit 8c76b2953f729a531cdacf8e25e0545c777cc500
0.04
commit 7689ca29253b28e6adbe77e8dfc52af21f462ddd
0.04
commit 3ae1e11595b7bc12a7f53fe24e532204612f9c6e
0.04
commit 81f4b9ae83475508b2fe2055b0a77b30b095006e
0.04
commit d26b797f12858aab31d05fd87e181e92d1e48a93
0.04
commit 58a1cdbc6cc8bb64bebbc3d1a74676c5f0123d96
0.04
commit 484fde8cb05e890e655e935a72cd48042f749b7a
0.04
```
