import os
import helpers

class SwiftFile:
    def __init__(self, framework_name, loc, imports, interfaces, structs, classes, methods, n_of_comments):
        self.framework_name = framework_name
        self.loc = loc
        self.imports = imports
        self.interfaces = interfaces
        self.structs = structs
        self.classes = classes
        self.methods = methods
        self.n_of_comments = n_of_comments


class SwiftFileParser:
    def __init__(self, file, base_path):
        self.file = file
        self.base_path = base_path
        self.imports = []
        self.attributes_modifiers = [
            'private',
            'fileprivate',
            'internal',
            'public',
            'final',
            'open'
        ]

    def parse(self):
        n_of_comments = 0
        loc=0

        attributes_regex_map = {
            helpers.ParsingHelpers.IMPORTS: [],
            helpers.ParsingHelpers.PROTOCOLS: [],
            helpers.ParsingHelpers.STRUCTS: [],
            helpers.ParsingHelpers.CLASSES: []
        }

        methods=[]
        commented_line = False
        with open(self.file) as f:
            for line in f:
                trimmed = line.strip()
                if len(trimmed) == 0:
                    continue

                # Comments
                if helpers.ParsingHelpers.check_existence(helpers.ParsingHelpers.SINGLE_COMMENT, trimmed):
                    n_of_comments += 1
                    continue

                if helpers.ParsingHelpers.check_existence(helpers.ParsingHelpers.BEGIN_COMMENT, trimmed):
                    commented_line = True
                    n_of_comments += 1

                if helpers.ParsingHelpers.check_existence(helpers.ParsingHelpers.END_COMMENT, trimmed):
                    if commented_line == False:
                        n_of_comments += 1
                    commented_line = False
                    continue

                if commented_line == True:
                    n_of_comments += 1
                    continue

                loc += 1

                for key, value in attributes_regex_map.items():
                    extracted_value = helpers.ParsingHelpers.extract_substring_with_pattern(key, trimmed)
                    if len(extracted_value) > 0:
                        value.append(extracted_value)
                        continue


        return SwiftFile(
            framework_name=self.__framework_name(),
            loc=loc,
            imports=attributes_regex_map[helpers.ParsingHelpers.IMPORTS],
            interfaces=attributes_regex_map[helpers.ParsingHelpers.PROTOCOLS],
            structs=attributes_regex_map[helpers.ParsingHelpers.STRUCTS],
            classes=attributes_regex_map[helpers.ParsingHelpers.CLASSES],
            methods=methods,
            n_of_comments=n_of_comments
        )

    # Properties mapper

    def __framework_name(self):
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath(subdir)
        if first_subpath.endswith('.swift'):
            return 'AppTarget'
        else:
            return first_subpath

    def __read_methods(self):
        return self.__read_attribute('func', ['', 'static'])

    # Private helpers

    def __extract_first_subpath(self, subdir):
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath(subdirs[0])
        else:
            return subdir.replace('/', '')

    def __read_attribute(self, attr_name, prefixed_attributes=None):
        """
        Extracts the attribute with a name from a line of the file, if exists
        @param attr_name: The attribute inspected (e.g. `class`, `protocol`)
        @param prefixed_attributes: The list of prefixed attributes to ignore
        @return: list of attributes matching the given pattern in the file
        """
        if prefixed_attributes is None:
            prefixed_attributes = []
        attrs = []
        with open(self.file) as f:
            for line in f:
                trimmed = line.strip()
                for a in prefixed_attributes:
                    trimmed = trimmed.replace(a, '')
                if trimmed.strip().startswith(attr_name):
                    attr = trimmed.replace(attr_name, '').strip()
                    attrs.append(attr)
        return attrs

