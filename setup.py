import setuptools

setuptools.setup(
    name="benchmcmc",
    packages=["benchmcmc"],
    description="Use MCMC to do benchmark analysis",
    license="MIT",
    version="0.0.1",
    install_requires=["matplotlib", "pymc3"],
    entry_points={"console_scripts": ["benchmcmc=benchmcmc:main"]},
)
