import setuptools

setuptools.setup(
    name="benchmcmc",
    packages=["benchmcmc"],
    version="0.0.0",
    install_requires=["matplotlib", "pymc3"],
    entry_points={"console_scripts": ["benchmcmc=benchmcmc:main"]},
)
