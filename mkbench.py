#!/usr/bin/env python

import random


def generate(n, mu, sigma):
    for i in range(n):
        yield random.gauss(mu, sigma)


def main():
    import sys

    if len(sys.argv) != 7:
        sys.exit("Usage: mkbench n1 mu1 sig1 n2 mu2 sig2")
    n1, m1, s1, n2, m2, s2 = [float(e) for e in sys.argv[1:]]
    for e in generate(round(n1), m1, s2):
        print(e)
    for e in generate(round(n2), m2, s2):
        print(e)


if __name__ == "__main__":
    main()
