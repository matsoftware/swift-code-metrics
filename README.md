# swift-code-metrics [![Build Status](https://travis-ci.org/matsoftware/swift-code-metrics.svg?branch=master)](https://travis-ci.org/matsoftware/swift-code-metrics)

Code metrics analyzer for Swift projects.

## Introduction

The goal of this software is to provide an insight of the architectural state of a software written in `Swift` that consists in several modules. 
Inspired by the book of Robert C. Martin, _Clean Architecture_, the software will scan the project to identify the different components in order to assess:
- the overall number of concrete classes and interfaces
- the _instability_ and _abstractness_ of the framework
- the _distance from the main sequence_
In addition, several common code metrics in the software industries are provided as part of the analysis, such as:
- LOC (Lines Of Code)
- NOC (Numbers Of Comments)
- POC (Percentage Of Comments)
- NBM (Number of Methods)
- Number of concretes (Number of classes and structs)
- NOT (Number Of Tests)

## Requirements

This is a _Python 3_ script that depends on _matplotlib_ and _adjustText_.

## Usage

The package is available on `pip` with `pip3 install swift-code-metrics`.

The syntax is:

`swift-code-metrics --source <path-to-swift-project> --artifacts <output-directory> --exclude <excluded-folders> --generate-graphs`

- `--source` is the path to the folder that contains the main Xcode project or Workspace
- `--artifacts` path to the folder that will contain the generated `output.json` report
- `--excluded` (optional) space separated list of path substrings to exclude from analysis (e.g. `Tests` will ignore all files/folders that contain `Tests`)
- `--tests-paths` (default: `Test Tests`) space separated list of path substrings matching test classes
- `--generate-graphs` (optional) if passed, it will generate the graphs related to the analysis and save them in the artifacts folder

A sample project is provided in the `resources` folder; example:

`python3 swift-code-metrics-runner.py --source tests/test_resources/ExampleProject/SwiftCodeMetricsExample --artifacts report --generate-graphs`

### Output format

The `output.json` file will contain the metrics related to all frameworks 
and an _aggregate_ result for the project. 

The example below is available [here](tests/test_resources/expected_output.json).

```json
{
    "non-test-frameworks": [
        {
            "BusinessLogic": {
                "loc": 49,
                "noc": 7,
                "poc": 12.5,
                "n_a": 0,
                "n_c": 3,
                "nbm": 3,
                "analysis": "The code is under commented. Low abstract component, few interfaces. ",
                "not": 0,
                "fan_in": 1,
                "fan_out": 2,
                "i": 0.667,
                "a": 0.0,
                "d_3": 0.333
            }
        },
        
        ...
        
    ],
    "tests-frameworks": [
        {
            "BusinessLogic_Test": {
                "loc": 7,
                "noc": 7,
                "poc": 50.0,
                "n_a": 0,
                "n_c": 1,
                "nbm": 1,
                "analysis": "The code is over commented. ",
                "not": 1
            }
        },
        
        ...
        
        
    ],
    "aggregate": {
        "non-test-frameworks": {
            "loc": 97,
            "noc": 35,
            "n_a": 1,
            "n_c": 7,
            "nbm": 10,
            "not": 0,
            "poc": 26.515
        },
        "tests-frameworks": {
            "loc": 53,
            "noc": 28,
            "n_a": 0,
            "n_c": 4,
            "nbm": 7,
            "not": 5,
            "poc": 34.568
        },
        "total": {
            "loc": 150,
            "noc": 63,
            "n_a": 1,
            "n_c": 11,
            "nbm": 17,
            "not": 5,
            "poc": 29.577
        }
    }
}
```

Legend:

|    Key    |              Metric              |                                             Description                                             |
|:---------:|:--------------------------------:|:---------------------------------------------------------------------------------------------------:|
|   `loc`   |           Lines Of Code          |                            Number of lines of code (empty lines excluded)                           |
|   `noc`   |        Number of Comments        |                                          Number of comments                                         |
|   `poc`   |      Percentage of Comments      |                                       100 * noc / ( noc + loc)                                      |
|  `fan_in` |              Fan-In              | Incoming dependencies: number of classes  outside the framework that depend on classes  inside it.  |
| `fan_out` |              Fan-Out             | Outgoing dependencies: number of classes  inside this component that depend on classes  outside it. |
|    `i`    |            Instability           |                                   I = fan_out / (fan_in + fan_out)                                  |
|   `n_a`   |        Number of abstracts       |                                 Number of protocols in the framework                                |
|   `n_c`   |        Number of concretes       |                            Number of struct and classes in the framework                            |
|    `a`    |           Abstractness           |                                            A = n_a / n_c                                            |
|   `d_3`   | Distance from  the main sequence |                                             D³ = abs( A + I - 1 )                                   |
|   `nbm`   |         Number of methods        |                              Number of `func` (computed `var` excluded)                             |
|   `not`   |          Number of tests         |                      Number of methods in test frameworks starting with `test`                      |

## Current limitations

- This tool is designed for medium/large codebases composed by different frameworks. 
The script will scan the directory and it will identify the frameworks by the name of the 'root' folder, so it's strictly dependent on the file hierarchy.

- Libraries built with `spm` are not supported.

- The framework name is inferred using the directory structure. If the file is in the root dir, the `default_framework_name` will be used. No inspection of the xcodeproj will be made.

- The list of methods currently doesn't support computed vars

- Inline comments in code (such as `struct Data: {} //dummy data`) are currently not supported

- Only `XCTest` test frameworks are currently supported

## TODOs

- Code improvements
- Other (open to suggestions)

## Contact

[Mattia Campolese](https://www.linkedin.com/in/matcamp/)
