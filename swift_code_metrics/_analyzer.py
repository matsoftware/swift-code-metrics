import os
import json
from ._helpers import ReportingHelpers
from ._parser import SwiftFileParser
from ._metrics import Framework, Metrics


class Inspector:
    def __init__(self, directory, artifacts, exclude_paths=None):
        if exclude_paths is None:
            exclude_paths = []
        self.frameworks = []
        if directory is not None:
            self._analyze_directory(directory, exclude_paths)
            self.report = self._generate_report()
            self._save_report(artifacts)

    def _generate_report(self):
        report = {
            "frameworks": list(),
            "global": {
                "loc": 0,
                "noc": 0,
                "n_a": 0,
                "n_c": 0,
                "nbm": 0
            }
        }
        for f in self.frameworks:
            report["frameworks"].append(self.__framework_analysis(f))
            report["global"]["loc"] += f.loc
            report["global"]["noc"] += f.noc
            report["global"]["n_a"] += f.number_of_interfaces
            report["global"]["n_c"] += f.number_of_concrete_data_structures
            report["global"]["nbm"] += f.number_of_methods

        report["global"]["poc"] = \
            ReportingHelpers.decimal_format(Metrics.percentage_of_comments(report["global"]["noc"],
                                                                           report["global"]["loc"]))

        return report

    def _save_report(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, 'output.json'), 'w') as fp:
            json.dump(self.report, fp, indent=4)

    # Analysis

    def __framework_analysis(self, framework):
        """
        :param framework: The framework to analyze
        :return: The architectural analysis of the framework
        """
        loc = framework.loc
        noc = framework.noc
        poc = Metrics.percentage_of_comments(framework.noc, framework.loc)
        poc_analysis = Metrics.poc_analysis(poc)
        fan_in = Metrics.fan_in(framework, self.frameworks)
        fan_out = Metrics.fan_out(framework)
        i = Metrics.instability(framework, self.frameworks)
        n_a = framework.number_of_interfaces
        n_c = framework.number_of_concrete_data_structures
        a = Metrics.abstractness(framework)
        d_3 = Metrics.distance_main_sequence(framework, self.frameworks)
        nbm = framework.number_of_methods
        ia_analysis = Metrics.ia_analysis(i, a)
        return {
            framework.name: {
                "loc": loc,
                "noc": noc,
                "poc": ReportingHelpers.decimal_format(poc),
                "fan_in": fan_in,
                "fan_out": fan_out,
                "i": ReportingHelpers.decimal_format(i),
                "n_a": n_a,
                "n_c": n_c,
                "a": ReportingHelpers.decimal_format(a),
                "d_3": ReportingHelpers.decimal_format(d_3),
                "nbm": nbm,
                "analysis": poc_analysis + "\n" + ia_analysis
            }
        }

    def instability(self, framework):
        return Metrics.instability(framework, self.frameworks)

    def abstractness(self, framework):
        return Metrics.abstractness(framework)

    # Directory inspection

    def _analyze_directory(self, directory, exclude_paths):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.swift') and not self.__is_excluded_folder(subdir, exclude_paths):
                    full_path = os.path.join(subdir, file)
                    swift_file = SwiftFileParser(full_path, directory).parse()
                    self.__append_dependency(swift_file)
        self.__cleanup_external_dependencies()

    def __is_excluded_folder(self, subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False

    def __append_dependency(self, swift_file):
        framework = self.__get_or_create_framework(swift_file.framework_name)
        framework.number_of_files += 1
        framework.loc += swift_file.loc
        framework.noc += swift_file.n_of_comments
        framework.number_of_interfaces += len(swift_file.interfaces)
        framework.number_of_concrete_data_structures += len(swift_file.structs + swift_file.classes)
        framework.number_of_methods += len(swift_file.methods)

        for f in swift_file.imports:
            imported_framework = self.__get_or_create_framework(f)
            if imported_framework is None:
                imported_framework = Framework(f)
            framework.append_import(imported_framework)

    def __cleanup_external_dependencies(self):
        # It will remove external dependencies built as source
        self.frameworks = list(filter(lambda f: f.number_of_files > 0, self.frameworks))

    def __get_or_create_framework(self, framework_name):
        framework = self.__get_framework(framework_name)
        if framework is None:
            # not found, create a new one
            framework = Framework(framework_name)
            self.frameworks.append(framework)
        return framework

    def __get_framework(self, name):
        for f in self.frameworks:
            if f.name == name:
                return f
        return None

