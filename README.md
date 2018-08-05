# swift-code-metrics

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

## Requirements

This is a _python3_ script that depends on _matplotlib_ (`pip3 install matplotlib`).

## Usage

The syntax is:

`python3 swift-code-analyzer.py <path-to-swift-project> --exclude <excluded-folders> --artifacts <output-directory>`

- `<path-to-swift-project>` is the path to the folder that contains the main Xcode project or Workspace
- `<excluded-folders>` (optional) list of subdirectories to exclude from analysis (e.g. `ThirdParty Carthage Pods`)
- `<output-directory>` (optional) path to the folder that will contain the generated textual analysis and graphs; if empty, the software will show the images to the user and print the report to the console


## Current limitations

- This tool is designed for medium/large codebases composed by different frameworks. 
The script will scan the directory and it will identify the frameworks by the name of the 'root' folder, so it's strictly dependent on the file hierarchy.

- Libraries built with `spm` are not supported.

- The framework name is inferred using the directory structure. If the file is in the root dir, the
          `default_framework_name` will be used. No inspection of the xcodeproj will be made.

- The list of methods currently doesn't support computed vars

- Inline comments in code (such as `struct Data: {} //dummy data`) are currently not supported

## TODOs

- Code improvements
- Other (open to suggestions)

## Contact

[Mattia Campolese](https://www.linkedin.com/in/matcamp/)
