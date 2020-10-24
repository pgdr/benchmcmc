#!/usr/bin/env python
"""This is a small script for generating synthetic benchmark data.

Essentially, you would run it like this:

$ python mkbench.py 100 15 3 100 14 3 [--beta] > benchmarkfile.txt

which generates 200 samples, 100 from N(mu=15, sigma=3) followed by 100
from N(mu=14, sigma=3).

"""

import random


def generate(n, mu, sigma, beta=False):
    for i in range(n):
        if beta:
            yield mu + sigma * random.betavariate(2, 5)  # good enough
        else:
            yield random.gauss(mu, sigma)


def main(args=None):
    import sys
    if args is None:
        args = sys.argv

    beta = "--beta" in args
    args = [a for a in args if a != "--beta"]

    if len(args) != 7:
        sys.exit("Usage: mkbench n1 mu1 sig1 n2 mu2 sig2 [--beta]")
    n1, m1, s1, n2, m2, s2 = [float(e) for e in args[1:]]
    for e in generate(round(n1), m1, s1, beta=beta):
        print(e)
    for e in generate(round(n2), m2, s2, beta=beta):
        print(e)


if __name__ == "__main__":
    main()
