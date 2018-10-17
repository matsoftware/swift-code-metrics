import os
from ._helpers import AnalyzerHelpers, ParsingHelpers


class SwiftFile:
    def __init__(self, framework_name, loc, imports, interfaces, structs, classes, methods, n_of_comments):
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
        """
        self.framework_name = framework_name
        self.loc = loc
        self.imports = imports
        self.interfaces = interfaces
        self.structs = structs
        self.classes = classes
        self.methods = methods
        self.n_of_comments = n_of_comments

    @property
    def tests(self):
        """
        List of test extracted from the parsed methods.
        :return: array of strings
        """
        return list(filter(lambda method: method.startswith(ParsingHelpers.TEST_METHOD_PREFIX),
                           self.methods))


class SwiftFileParser:
    def __init__(self, file, base_path, is_test=False):
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

    def parse(self):
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

        return SwiftFile(
            framework_name=self.__framework_name(),
            loc=loc,
            imports=self.attributes_regex_map[ParsingHelpers.IMPORTS],
            interfaces=self.attributes_regex_map[ParsingHelpers.PROTOCOLS],
            structs=self.attributes_regex_map[ParsingHelpers.STRUCTS],
            classes=self.attributes_regex_map[ParsingHelpers.CLASSES],
            methods=self.attributes_regex_map[ParsingHelpers.FUNCS],
            n_of_comments=n_of_comments
        )

    # Private helpers

    def __framework_name(self):
        suffix = ParsingHelpers.DEFAULT_TEST_FRAMEWORK_SUFFIX if self.is_test else ''
        return self.__extracted_framework_name() + suffix

    def __extracted_framework_name(self):
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath(subdir)
        if first_subpath.endswith(AnalyzerHelpers.SWIFT_FILE_EXTENSION):
            return ParsingHelpers.DEFAULT_FRAMEWORK_NAME
        else:
            return first_subpath

    def __extract_first_subpath(self, subdir):
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath(subdirs[0])
        else:
            return subdir.replace('/', '')
