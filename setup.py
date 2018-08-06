import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swift-code-analyzer",
    version="0.5",
    author="Mattia Campolese",
    author_email="matsoftware@gmail.com",
    description="Code metrics analyzer for Swift projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matsoftware/swift-code-metrics",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)