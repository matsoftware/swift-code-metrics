from typing import Dict, List
from ._helpers import ReportingHelpers
from ._metrics import FrameworkData, Framework, Metrics
from ._parser import SwiftFile


class ReportProcessor:

    @staticmethod
    def generate_report(frameworks: List['Framework'], shared_files: Dict[str, 'SwiftFile']):
        report = Report()

        # Shared files
        for _, shared_files in shared_files.items():
            shared_file = shared_files[0]
            shared_file_data = FrameworkData.from_swift_file(swift_file=shared_file)
            for _ in range((len(shared_files) - 1)):
                report.shared_code += shared_file_data
                report.total_aggregate -= shared_file_data
                if shared_file.is_test:
                    report.test_framework_aggregate -= shared_file_data
                else:
                    report.non_test_framework_aggregate -= shared_file_data

        # Frameworks
        for f in sorted(frameworks, key=lambda fr: fr.name, reverse=False):
            analysis = ReportProcessor.__framework_analysis(f, frameworks)
            if f.is_test_framework:
                report.tests_framework.append(analysis)
                report.test_framework_aggregate.append_framework(f)
            else:
                report.non_test_framework.append(analysis)
                report.non_test_framework_aggregate.append_framework(f)
            report.total_aggregate.append_framework(f)

        return report

    @staticmethod
    def __framework_analysis(framework: 'Framework', frameworks: List['Framework']) -> Dict:
        """
        :param framework: The framework to analyze
        :return: The architectural analysis of the framework
        """
        framework_data = framework.data
        loc = framework_data.loc
        noc = framework_data.noc
        poc = Metrics.percentage_of_comments(framework_data.noc,
                                             framework_data.loc)
        analysis = Metrics.poc_analysis(poc)
        n_a = framework_data.number_of_interfaces
        n_c = framework_data.number_of_concrete_data_structures
        nom = framework_data.number_of_methods
        dependencies = Metrics.total_dependencies(framework)
        n_of_tests = framework_data.number_of_tests
        n_of_imports = framework.number_of_imports

        # Non-test framework analysis
        non_test_analysis = {}
        if not framework.is_test_framework:
            non_test_analysis["fan_in"] = Metrics.fan_in(framework, frameworks)
            non_test_analysis["fan_out"] = Metrics.fan_out(framework)
            i = Metrics.instability(framework, frameworks)
            a = Metrics.abstractness(framework)
            non_test_analysis["i"] = ReportingHelpers.decimal_format(i)
            non_test_analysis["a"] = ReportingHelpers.decimal_format(a)
            non_test_analysis["d_3"] = ReportingHelpers.decimal_format(
                Metrics.distance_main_sequence(framework, frameworks))
            analysis += Metrics.ia_analysis(i, a)

        base_analysis = {
            "loc": loc,
            "noc": noc,
            "poc": ReportingHelpers.decimal_format(poc),
            "n_a": n_a,
            "n_c": n_c,
            "nom": nom,
            "not": n_of_tests,
            "noi": n_of_imports,
            "analysis": analysis,
            "dependencies": dependencies,
            "submodules": framework.submodule.as_dict
        }

        return {
            framework.name: {**base_analysis, **non_test_analysis}
        }


class Report:
    def __init__(self):
        self.non_test_framework = list()
        self.tests_framework = list()
        self.non_test_framework_aggregate = FrameworkData()
        self.test_framework_aggregate = FrameworkData()
        self.total_aggregate = FrameworkData()
        self.shared_code = FrameworkData()
        # Constants for report
        self.non_test_frameworks_key = "non-test-frameworks"
        self.tests_frameworks_key = "tests-frameworks"
        self.aggregate_key = "aggregate"
        self.shared_key = "shared"
        self.total_key = "total"

    @property
    def as_dict(self) -> Dict:
        return {
            self.non_test_frameworks_key: self.non_test_framework,
            self.tests_frameworks_key: self.tests_framework,
            self.shared_key: self.shared_code.as_dict,
            self.aggregate_key: {
                self.non_test_frameworks_key: self.non_test_framework_aggregate.as_dict,
                self.tests_frameworks_key: self.test_framework_aggregate.as_dict,
                self.total_key: self.total_aggregate.as_dict
            }
        }

