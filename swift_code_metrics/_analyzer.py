import os
import json

from ._helpers import AnalyzerHelpers
from ._parser import SwiftFileParser, SwiftFile
from ._metrics import Framework, SubModule
from ._report import ReportProcessor
from functional import seq
from typing import List, Optional


class Inspector:
    def __init__(self, directory: str, artifacts: str, tests_default_suffixes: List[str], exclude_paths: List[str]):
        self.exclude_paths = exclude_paths
        self.directory = directory
        self.artifacts = artifacts
        self.tests_default_suffixes = tests_default_suffixes
        self.frameworks = []
        self.shared_code = {}
        self.report = None

    def analyze(self) -> bool:
        if self.directory is not None:
            # Initialize report
            self.__analyze_directory(self.directory, self.exclude_paths, self.tests_default_suffixes)
            if len(self.frameworks) > 0:
                self.report = ReportProcessor.generate_report(self.frameworks, self.shared_code)
                self._save_report(self.artifacts)
                return True
        return False

    def filtered_frameworks(self, is_test=False) -> List['Framework']:
        return seq(self.frameworks) \
            .filter(lambda f: f.is_test_framework == is_test) \
            .list()

    def _save_report(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, 'output.json'), 'w') as fp:
            json.dump(self.report.as_dict, fp, indent=4)

    # Directory inspection

    def __analyze_directory(self, directory: str, exclude_paths: List[str], tests_default_paths: List[str]):
        for subdir, _, files in os.walk(directory):
            for file in files:
                if file.endswith(AnalyzerHelpers.SWIFT_FILE_EXTENSION) and \
                        not AnalyzerHelpers.is_path_in_list(subdir, exclude_paths):
                    full_path = os.path.join(subdir, file)
                    swift_files = SwiftFileParser(file=full_path,
                                                  base_path=directory,
                                                  current_subdir=subdir,
                                                  tests_default_paths=tests_default_paths).parse()
                    for swift_file in swift_files:
                        self.__append_dependency(swift_file)
                        self.__process_shared_file(swift_file, full_path)

        self.__cleanup_external_dependencies()

    def __append_dependency(self, swift_file: 'SwiftFile'):
        framework = self.__get_or_create_framework(swift_file.framework_name)
        Inspector.__populate_submodule(framework=framework, swift_file=swift_file)
        # This covers the scenario where a test framework might contain no tests
        framework.is_test_framework = swift_file.is_test

        for f in swift_file.imports:
            imported_framework = self.__get_or_create_framework(f)
            if imported_framework is None:
                imported_framework = Framework(f)
            framework.append_import(imported_framework)

    @staticmethod
    def __populate_submodule(framework: 'Framework', swift_file: 'SwiftFile'):
        current_paths = str(swift_file.path).split('/')
        paths = list(reversed(current_paths))

        submodule = framework.submodule
        while len(paths) > 1:
            path = paths.pop()
            submodules = [s for s in submodule.submodules]
            existing_submodule = seq(submodules).filter(lambda sm: sm.name == path)
            if len(list(existing_submodule)) > 0:
                submodule = existing_submodule.first()
            else:
                new_submodule = SubModule(name=path, files=[], submodules=[], parent=submodule)
                submodule.submodules.append(new_submodule)
                submodule = new_submodule

        submodule.files.append(swift_file)

    def __process_shared_file(self, swift_file: 'SwiftFile', directory: str):
        if not swift_file.is_shared:
            return

        if not self.shared_code.get(directory):
            self.shared_code[directory] = [swift_file]
        else:
            self.shared_code[directory].append(swift_file)

    def __cleanup_external_dependencies(self):
        # It will remove external dependencies built as source
        self.frameworks = seq(self.frameworks) \
            .filter(lambda f: f.number_of_files > 0) \
            .list()

    def __get_or_create_framework(self, framework_name: str) -> 'Framework':
        framework = self.__get_framework(framework_name)
        if framework is None:
            # not found, create a new one
            framework = Framework(framework_name)
            self.frameworks.append(framework)
        return framework

    def __get_framework(self, name: str) -> Optional['Framework']:
        for f in self.frameworks:
            if f.name == name:
                return f
        return None
