[![Build Status](https://travis-ci.org/matsoftware/swift-code-metrics.svg?branch=master)](https://travis-ci.org/matsoftware/swift-code-metrics) [![codecov](https://codecov.io/gh/matsoftware/swift-code-metrics/branch/master/graph/badge.svg)](https://codecov.io/gh/matsoftware/swift-code-metrics) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ff12e0cafce4ec68024d47b000d2e42)](https://app.codacy.com/app/matsoftware/swift-code-metrics?utm_source=github.com&utm_medium=referral&utm_content=matsoftware/swift-code-metrics&utm_campaign=Badge_Grade_Dashboard)
[![PyPI](https://img.shields.io/pypi/v/swift-code-metrics.svg)](https://pypi.python.org/pypi/swift-code-metrics) [![License](https://img.shields.io/badge/license-MIT-blue.svg?x=1)](LICENSE)

# swift-code-metrics

Code metrics analyzer for Swift projects.

## Introduction

The goal of this software is to provide an insight of the architectural state of a software written in `Swift` that consists in several modules.
Inspired by the book of Robert C. Martin, _Clean Architecture_, the software will scan the project to identify the different components in order to assess several common code metrics in the software industry:
-   the overall number of concrete classes and interfaces
-   the _instability_ and _abstractness_ of the framework
-   the _distance from the main sequence_
-   LOC (Lines Of Code)
-   NOC (Numbers Of Comments)
-   POC (Percentage Of Comments)
-   NBM (Number of Methods)
-   Number of concretes (Number of classes and structs)
-   NOT (Number Of Tests)
-   NOI (Number Of Imports)
-   Frameworks dependency graph (number of internal and external dependencies)

## Requirements

This is a _Python 3_ script that depends on _matplotlib_, _adjustText_, __pyfunctional__ and _pygraphviz_.

This latest package depends on the [Graphviz](https://www.graphviz.org/download/) binary that must be installed.

## Usage

The package is available on `pip` with `pip3 install swift-code-metrics`.

The syntax is:

`swift-code-metrics --source <path-to-swift-project> --artifacts <output-directory> --exclude <excluded-folders> --tests-paths <test-paths> --generate-graphs`

-   `--source` is the path to the folder that contains the main Xcode project or Workspace
-   `--artifacts` path to the folder that will contain the generated `output.json` report
-   `--excluded` (optional) space separated list of path substrings to exclude from analysis (e.g. `Tests` will ignore all files/folders that contain `Tests`)
-   `--tests-paths` (default: `Test Tests`) space separated list of path substrings matching test classes
-   `--generate-graphs` (optional) if passed, it will generate the graphs related to the analysis and save them in the artifacts folder

## Documentation

Please follow the [guide](docs/GUIDE.md) with a practical example to get started.

## Current limitations

-   This tool is designed for medium/large codebases composed by different frameworks.
The script will scan the directory and it will identify the frameworks by the name of the 'root' folder, so it's strictly dependent on the file hierarchy.

-   Libraries built with `spm` are not supported.

-   The framework name is inferred using the directory structure. If the file is in the root dir, the `default_framework_name` will be used. No inspection of the xcodeproj will be made.

-   The list of methods currently doesn't support computed vars

-   Inline comments in code (such as `struct Data: {} //dummy data`) are currently not supported

-   Only `XCTest` test frameworks are currently supported

## TODOs

-   Code improvements
-   Other (open to suggestions)

## Contact

[Mattia Campolese](https://www.linkedin.com/in/matcamp/)
