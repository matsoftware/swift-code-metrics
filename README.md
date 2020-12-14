[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmatsoftware%2Fswift-code-metrics.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmatsoftware%2Fswift-code-metrics?ref=badge_shield) [![License](https://img.shields.io/badge/license-MIT-blue.svg?x=1)](LICENSE) [![Build Status](https://travis-ci.org/matsoftware/swift-code-metrics.svg?branch=master)](https://travis-ci.org/matsoftware/swift-code-metrics) [![codecov](https://codecov.io/gh/matsoftware/swift-code-metrics/branch/master/graph/badge.svg)](https://codecov.io/gh/matsoftware/swift-code-metrics) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ff12e0cafce4ec68024d47b000d2e42)](https://app.codacy.com/app/matsoftware/swift-code-metrics?utm_source=github.com&utm_medium=referral&utm_content=matsoftware/swift-code-metrics&utm_campaign=Badge_Grade_Dashboard)
[![PyPI](https://img.shields.io/pypi/v/swift-code-metrics.svg)](https://pypi.python.org/pypi/swift-code-metrics)

# swift-code-metrics

Code metrics analyzer for Swift projects.

| ![Example code distribution](https://raw.githubusercontent.com/matsoftware/swift-code-metrics/master/docs/assets/code_distribution.jpeg) ![Example deviation main sequence](https://raw.githubusercontent.com/matsoftware/swift-code-metrics/master/docs/assets/example_deviation_main_sequence.jpeg) |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Example internal distribution](https://raw.githubusercontent.com/matsoftware/swift-code-metrics/master/docs/assets/example_internal_deps_graph.jpeg)                                                                                                                                                |

## Introduction

The goal of this software is to provide an insight of the architectural state of a software written in `Swift` that consists in several modules.
Inspired by the book of Robert C. Martin, _Clean Architecture_, the software will scan the project to identify the different components in order to assess several common code metrics in the software industry:

-   the overall number of concrete classes and interfaces
-   the _instability_ and _abstractness_ of the framework
-   the _distance from the main sequence_
-   LOC (Lines Of Code)
-   NOC (Numbers Of Comments)
-   POC (Percentage Of Comments)
-   NOM (Number of Methods)
-   Number of concretes (Number of classes and structs)
-   NOT (Number Of Tests)
-   NOI (Number Of Imports)
-   Frameworks dependency graph (number of internal and external dependencies)

## Requirements

This is a _Python 3_ script that depends on _matplotlib_, _adjustText_, _pyfunctional_ and _pygraphviz_.

This latest package depends on the [Graphviz](https://www.graphviz.org/download/) binary that must be installed.

## Usage

The package is available on `pip` with `pip3 install swift-code-metrics`.

The syntax is:

`swift-code-metrics --source <path-to-swift-project> --artifacts <output-directory> --exclude <excluded-folders> --tests-paths <test-paths> --generate-graphs`

-   `--source` is the path to the folder that contains the main Xcode project or Workspace
-   `--artifacts` path to the folder that will contain the generated `output.json` report
-   `--exclude` (optional) space separated list of path substrings to exclude from analysis (e.g. `Tests` will ignore all files/folders that contain `Tests`)
-   `--tests-paths` (default: `Test Tests`) space separated list of path substrings matching test classes
-   `--generate-graphs` (optional) if passed, it will generate the graphs related to the analysis and save them in the artifacts folder

## Documentation

Please follow the [guide](https://github.com/matsoftware/swift-code-metrics/tree/master/docs/GUIDE.md) with a practical example to get started.

## Current limitations

-   This tool is designed for medium/large codebases composed by different frameworks.
    The script will scan the directory and it will identify the frameworks by the name of the 'root' folder, 
    so it's strictly dependent on the file hierarchy (unless a [project path override file](docs/GUIDE.md#Project-paths-override) is specified)

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
