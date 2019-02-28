import os
from pathlib import Path
from typing import List
from ._helpers import AnalyzerHelpers, ParsingHelpers, JSONReader
from ._helpers import Log


class SwiftFile(object):
    def __init__(self, framework_name: List[str],
                 loc: int,
                 imports: List[str],
                 interfaces: List[str],
                 structs: List[str],
                 classes: List[str],
                 methods: List[str],
                 n_of_comments: int,
                 is_shared: bool):
        """
        Creates a SwiftFile instance that represents a parsed swift file.
        :param framework_name: The framework where the file belongs to.
        :param loc: Lines Of Code
        :param imports: List of imported frameworks
        :param interfaces: List of interfaces (protocols) defined in the file
        :param structs: List of structs defined in the file
        :param classes: List of classes defined in the file
        :param methods: List of functions defined in the file
        :param n_of_comments: Total number of comments in the file
        :param is_shared: True if the file is shared with other frameworks
        """
        self.framework_name = framework_name
        self.loc = loc
        self.imports = imports
        self.interfaces = interfaces
        self.structs = structs
        self.classes = classes
        self.methods = methods
        self.n_of_comments = n_of_comments
        self.is_shared = is_shared

    @property
    def tests(self) -> List[str]:
        """
        List of test extracted from the parsed methods.
        :return: array of strings
        """
        return list(filter(lambda method: method.startswith(ParsingHelpers.TEST_METHOD_PREFIX),
                           self.methods))


class ProjectPathsOverride(object):

    def __init__(self, **entries):
        self.__dict__ = entries['entries']

    def __eq__(self, other):
        return (self.libraries == other.libraries) and (self.shared == other.shared)

    @staticmethod
    def load_from_json(path: str) -> 'ProjectPathsOverride':
        return ProjectPathsOverride(entries=JSONReader.read_json_file(path))


class SwiftFileParser(object):
    def __init__(self, file: str, base_path: str, is_test=False):
        self.file = file
        self.base_path = base_path
        self.is_test = is_test
        self.imports = []
        self.attributes_regex_map = {
            ParsingHelpers.IMPORTS: [],
            ParsingHelpers.PROTOCOLS: [],
            ParsingHelpers.STRUCTS: [],
            ParsingHelpers.CLASSES: [],
            ParsingHelpers.FUNCS: [],
        }

    def parse(self) -> List['SwiftFile']:
        """
        Parses the .swift file to inspect the code inside.
        Notes:
        - The framework name is inferred using the directory structure. If the file is in the root dir, the
          `default_framework_name` will be used. No inspection of the xcodeproj will be made.
        - The list of methods currently doesn't support computed vars
        - Inline comments in code (such as `struct Data: {} //dummy data`) are currently not supported
        :return: an instance of SwiftFile with the result of the parsing of the provided `file`
        """
        n_of_comments = 0
        loc = 0

        commented_line = False
        with open(self.file, encoding='utf-8') as f:
            for line in f:
                trimmed = line.strip()
                if len(trimmed) == 0:
                    continue

                # Comments
                if ParsingHelpers.check_existence(ParsingHelpers.SINGLE_COMMENT, trimmed):
                    n_of_comments += 1
                    continue

                if ParsingHelpers.check_existence(ParsingHelpers.BEGIN_COMMENT, trimmed):
                    commented_line = True
                    n_of_comments += 1

                if ParsingHelpers.check_existence(ParsingHelpers.END_COMMENT, trimmed):
                    if not commented_line:
                        n_of_comments += 1
                    commented_line = False
                    continue

                if commented_line:
                    n_of_comments += 1
                    continue

                loc += 1

                for key, value in self.attributes_regex_map.items():
                    extracted_value = ParsingHelpers.extract_substring_with_pattern(key, trimmed)
                    if len(extracted_value) > 0:
                        value.append(extracted_value)
                        continue

        framework_names = self.__extract_framework_names()
        is_shared_file = len(framework_names) > 1
        return [SwiftFile(
            framework_name=f,
            loc=loc,
            imports=self.attributes_regex_map[ParsingHelpers.IMPORTS],
            interfaces=self.attributes_regex_map[ParsingHelpers.PROTOCOLS],
            structs=self.attributes_regex_map[ParsingHelpers.STRUCTS],
            classes=self.attributes_regex_map[ParsingHelpers.CLASSES],
            methods=self.attributes_regex_map[ParsingHelpers.FUNCS],
            n_of_comments=n_of_comments,
            is_shared=is_shared_file
        ) for f in framework_names]

    # Private helpers

    def __extract_framework_names(self) -> List[str]:
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath(subdir)
        # Root folder files
        if first_subpath.endswith(AnalyzerHelpers.SWIFT_FILE_EXTENSION):
            return [ParsingHelpers.DEFAULT_FRAMEWORK_NAME]

        # Default folder configuration with no overrides
        project_override_path = Path(self.base_path) / first_subpath / ParsingHelpers.FRAMEWORK_STRUCTURE_OVERRIDE_FILE
        if not project_override_path.exists():
            return [self.__framework_name_from_path(first_subpath)]

        # Analysis of custom libraries folder
        file_parts = Path(self.file).parts
        project_override = ProjectPathsOverride.load_from_json(str(project_override_path))
        for name, framework_path in project_override.libraries.items():
            if framework_path in file_parts:
                return [name]
        # Analysis of shared folder
        for shared_path in project_override.shared:
            if shared_path in file_parts:
                return project_override.libraries.keys()

        # No overrides (wrong configuration)
        Log.warn(f'{self.file} not classified in a folder with projects overrides (scm.json).')
        return [self.__framework_name_from_path(first_subpath)]

    def __framework_name_from_path(self, path: str) -> str:
        suffix = ParsingHelpers.DEFAULT_TEST_FRAMEWORK_SUFFIX if self.is_test else ''
        return path + suffix

    def __extract_first_subpath(self, subdir: str) -> str:
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath(subdirs[0])
        else:
            return subdir.replace('/', '')
