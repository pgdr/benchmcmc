import statistics
import pymc3 as pm
import matplotlib.pyplot as plt
import logging
import numpy as np

SAMPLES = 20 * 1000
TUNE = 5 * 1000


def _mu_sig(data):
    mu = round(statistics.fmean(data), 2)
    sigma = max(round(statistics.stdev(data) * 2, 1), 0.1)
    return mu, sigma


def _set_up(benchmark, beta=False):
    N = len(benchmark)
    length = np.arange(N)

    mu1, sigma1 = _mu_sig(benchmark[: N // 3])
    mu2, sigma2 = _mu_sig(benchmark[2 * (N // 3) :])
    print(f"Prior: Normal(N={N//2}, mu={mu1}, sigma={sigma1})")
    print(f"Prior: Normal(N={N//2}, mu={mu2}, sigma={sigma2})")

    with pm.Model() as benchmark_model:
        switchpoint = pm.DiscreteUniform("switchpoint", lower=0, upper=len(length))
        benchmark_1 = pm.Normal("benchmark_1", mu=mu1, sigma=sigma1)
        benchmark_2 = pm.Normal("benchmark_2", mu=mu2, sigma=sigma2)
        rate = pm.math.switch(switchpoint >= length, benchmark_1, benchmark_2)
        benchmark_distribution = pm.Normal("benchmarks", rate, observed=benchmark)
    return benchmark_model, ["benchmark_1", "benchmark_2", "switchpoint"]


def _run_model(model):
    with model:
        return pm.sample(draws=SAMPLES, tune=TUNE)


def run_benchmark(data):
    model, variables = _set_up(data)
    trace = _run_model(model)

    with model:
        pm.traceplot(trace, variables)

    plt.show()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit("Usage: benchmark.py benchfile")

    with open(sys.argv[1], "r") as fin:
        data = [float(x) for x in fin.readlines()]
    run_benchmark(data)
