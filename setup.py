import setuptools
from swift_code_metrics.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "matplotlib > 2",
    "adjustText",
    "pygraphviz > 1.5",
    "pyfunctional > 1.2",
    "numpy > 1.22.0",
    "dataclasses"
]

setuptools.setup(
    name="swift-code-metrics",
    version=VERSION,
    author="Mattia Campolese",
    author_email="matsoftware@gmail.com",
    description="Code metrics analyzer for Swift projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matsoftware/swift-code-metrics",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*', 'test']),
    entry_points={
        "console_scripts": ['swift-code-metrics = swift_code_metrics.scm:main']
    },
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=install_requires
)
