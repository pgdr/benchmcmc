import os
import setuptools

__pgdr = "PG Drange <pgdr@equinor.com>"
__source = "https://github.com/pgdr/benchmcmc"
__webpage = __source
__description = "Use MCMC to do benchmark analysis"


def _src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))


def _read_file(fname, op):
    with open(_src(fname), "r") as fin:
        return op(fin.readlines())


def readme():
    try:
        return _read_file("README.md", lambda lines: "".join(lines))
    except Exception:
        return __description


setuptools.setup(
    name="benchmcmc",
    version="0.0.3",
    packages=["benchmcmc"],
    description=__description,
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="PG Drange",
    author_email="pgdr@equinor.com",
    maintainer=__pgdr,
    url=__webpage,
    project_urls={
        "Bug Tracker": "{}/issues".format(__source),
        "Documentation": "{}/blob/master/README.md".format(__source),
        "Source Code": __source,
    },
    license="MIT",
    keywords="mcmc, bayesian methods, statistics, benchmark analysis, disaster modeling, unix, command line tool",
    install_requires=["matplotlib", "pymc3"],
    entry_points={"console_scripts": ["benchmcmc=benchmcmc:main"]},
)
