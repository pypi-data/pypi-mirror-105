from setuptools import setup, find_packages

VERSION = '0.0.02'
DESCRIPTION = 'TimeSeriesSimulation'
LONG_DESCRIPTION = 'A Package for Agent Based Time Series Modeling'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="TimeSeriesSimulator",
    version=VERSION,
    author="Thomas Meli",
    author_email="<tpmeli@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages

    keywords=['python', 'time series', 'simulator', 'agent'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)