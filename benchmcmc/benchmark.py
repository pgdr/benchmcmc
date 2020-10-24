import sys
import statistics

import pymc3 as pm
import matplotlib.pyplot as plt


def _mu_sig(data):
    mu = round(statistics.fmean(data), 2)
    sigma = max(round(statistics.stdev(data) * 2, 1), 0.1)
    return mu, sigma


def _set_up(benchmark, beta=False):
    N = len(benchmark)
    length = list(range(N))

    sample_N = min(30, N//3)
    if sample_N < 10:
        sample_N = N//2

    mu1, sigma1 = _mu_sig(benchmark[: sample_N])
    mu2, sigma2 = _mu_sig(benchmark[(N-sample_N):])
    print(f"Prior: Normal(N={sample_N}, mu={mu1}, sigma={sigma1})")
    print(f"Prior: Normal(N={sample_N}, mu={mu2}, sigma={sigma2})")

    with pm.Model() as benchmark_model:
        switchpoint = pm.DiscreteUniform("switchpoint", lower=0, upper=len(length))
        benchmark_1 = pm.Normal("benchmark_1", mu=mu1, sigma=sigma1)
        benchmark_2 = pm.Normal("benchmark_2", mu=mu2, sigma=sigma2)
        rate = pm.math.switch(switchpoint >= length, benchmark_1, benchmark_2)
        benchmark_distribution = pm.Normal("benchmarks", rate, observed=benchmark)
    return benchmark_model, ["benchmark_1", "benchmark_2", "switchpoint"]


def _run_model(model, draws=None, tune=None):
    if not draws:
        draws = 1000
    if not tune:
        tune = 1000

    with model:
        return pm.sample(draws=draws, tune=tune)


def run_benchmark(data, draws=None, tune=None):
    model, variables = _set_up(data)
    trace = _run_model(model, draws, tune)

    with model:
        pm.traceplot(trace, variables)

    plt.show()


def _get_args(lst, args):
    ret = {}
    for a in args:
        if f"--{a}" in lst:
            idx = sys.argv.index(f"--{a}")
            ret[a] = int(sys.argv[idx + 1])
            del lst[idx]
            del lst[idx]
    ddargs = [f"--{e}" for e in args]
    return ret, [elt for elt in lst if elt not in ddargs]


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Reads a file of numbers, one number per file.")
        print("Use --generate to create synthetic data")
        sys.exit()

    if "--generate" in sys.argv:
        from .mkbench import main as mkbench

        mkbench(args=[a for a in sys.argv if a != "--generate"])
        sys.exit()

    cfg, args = _get_args(sys.argv, ["draws", "tune"])
    draws = cfg.get("draws")
    tune = cfg.get("tune")

    if len(args) != 2:
        sys.exit("Usage: benchmark.py benchfile [--draws nd] [--tune nt]")
    with open(args[1], "r") as fin:
        data = [float(x) for x in fin.readlines()]
    run_benchmark(data, draws=draws, tune=tune)


if __name__ == "__main__":
    main()
