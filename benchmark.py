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


def _set_up(data1, data2):
    mu1, sigma1 = _mu_sig(data1)
    mu2, sigma2 = _mu_sig(data2)
    benchmark = list(data1) + list(data2)
    length = np.arange(len(benchmark))

    logging.warning(f"Normal(N={len(data1)}, mu={mu1}, sigma={sigma1})")
    logging.warning(f"Normal(N={len(data2)}, mu={mu2}, sigma={sigma2})")

    with pm.Model() as benchmark_model:
        switchpoint = pm.DiscreteUniform("switchpoint", lower=0, upper=len(length))
        benchmark_1 = pm.Normal("benchmark_1", mu=mu1, sigma=sigma1)
        benchmark_2 = pm.Normal("benchmark_2", mu=mu2, sigma=sigma2)
        rate = pm.math.switch(switchpoint >= length, benchmark_1, benchmark_2)
        benchmark_distribution = pm.Normal("benchmarks", rate, observed=benchmark)
    return benchmark_model, ["benchmark_1", "benchmark_2", "switchpoint"]


def _run_model(model):
    with model:
        trace = pm.sample(draws=SAMPLES, tune=TUNE)
    return trace


def run_benchmark(data1, data2):
    model, variables = _set_up(data1, data2)
    trace = _run_model(model)

    with model:
        pm.traceplot(trace, variables)

    plt.show()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        sys.exit("Usage: benchmark.py bench1 bench2")

    with open(sys.argv[1], "r") as fin:
        data1 = [float(x) for x in fin.readlines()]
    with open(sys.argv[2], "r") as fin:
        data2 = [float(x) for x in fin.readlines()]
    run_benchmark(data1, data2)
