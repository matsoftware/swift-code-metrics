# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## UNRELEASED

### Added

-   Python 3.8 support

### Changed

-   The generated report is now containing a dictionary with sorted keys

### Fixed

-   [Issue#37](https://github.com/matsoftware/swift-code-metrics/issues/37) Support for M1 architecture
-   [Issue#34](https://github.com/matsoftware/swift-code-metrics/issues/34) Improved dependencies resolution

## [1.5.1](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.5.1) - 2020-02-09

### Fixed

-   [PR-32](https://github.com/matsoftware/swift-code-metrics/pull/32) Fix on dependencies version requirements

## [1.5.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.5.0) - 2020-10-06

### Added

-   [Issue-21](https://github.com/matsoftware/swift-code-metrics/issues/21) Recursive analysis of subdirectories (submodules) in frameworks

### Fixed

-   [PR-24](https://github.com/matsoftware/swift-code-metrics/pull/24) Fix on parsing import statements with complex comments

## [1.4.1](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.4.1) - 2020-07-29

### Added

-   [PR-22](https://github.com/matsoftware/swift-code-metrics/pull/22) Support for iOS 14 / macOS 11 frameworks

## [1.4.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.4.0) - 2020-02-25

### Added

-   [PR-17](https://github.com/matsoftware/swift-code-metrics/pull/17) Support for iOS 13 / Mac OSX 15 frameworks

### Fixed

-   [PR-11](https://github.com/matsoftware/swift-code-metrics/pull/11) Improved layout of bar plots for codebases with many frameworks
-   [Issue-12](https://github.com/matsoftware/swift-code-metrics/issues/12) `matplotlib` not initialized if `generate-graphs` is not passed
-   [Issue-19](https://github.com/matsoftware/swift-code-metrics/issues/19) Correctly parsing `@testable` imports and fix for test targets incorrectly counted in the `Fan-In` metric

## [1.3.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.3.0) - 2019-03-14

### Added

-   [PR-9](https://github.com/matsoftware/swift-code-metrics/pull/9) Support for multiple frameworks under the same project

### Fixed

-   [PR-10](https://github.com/matsoftware/swift-code-metrics/pull/9) Fixed issue when parsing paths with a repeating folder name

## [1.2.3](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.2.3) - 2019-02-19

### Fixed

-   [PR-6](https://github.com/matsoftware/swift-code-metrics/pull/6)
    Gracefully fail on empty projects or code without modules

## [1.2.2](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.2.2) - 2019-02-10

### Fixed

-   Renamed number of methods acronym (NBM > NOM)

## [1.2.1](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.2.1) - 2018-11-07

### Fixed

-   Small improvements in graphics legend
-   Fix for a redundant message in warnings
-   Updated documentation

## [1.2.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.2.0) - 2018-11-05

### Added

-   Added NOI (number of imports) metric and graph

### Changed

-   Improved dependency graphs by using a variable node and arrow thickness
-   Improved parsing of import statements
-   Improved bar charts' reports

### Fixed

-   Analysis of frameworks with no connection with the rest of the code will generate a warning
-   Improved code quality and test coverage

### Removed

-   Removed A, I and NBM graphs

## [1.1.2](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.1.2) - 2018-11-05

### Added

-   Added internal and external aggregate dependency graph

### Fixed

-   Renamed number of methods acronym (NBM > NOM)
-   Removed Apple frameworks from external dependencies

## [1.1.1](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.1.1) - 2018-10-23

### Added

-   Added list of dependencies in output.json

### Fixed

-   Supporting minimal setup of graphviz (fallback on SVG export for the dependency graph)

## [1.1.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.1.0) - 2018-10-22

### Added

-   Added support to test classes and frameworks with number of tests report and graph
-   Added frameworks dependency graph
-   Added code distribution chart

### Fixed

-   Improved graphs quality
-   Updated sample project to Xcode 10 / Swift 4.2
-   Extended test coverage
-   Updated documentation

## [1.0.1](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.0.1) - 2018-09-12

### Fixed

-   Enforced UTF-8 encoding on file opening

## [1.0.0](https://github.com/matsoftware/swift-code-metrics/releases/tag/1.0.0) - 2018-09-11

-   First stable release
