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
        self.attributes_regex_map = {
            helpers.ParsingHelpers.IMPORTS: [],
            helpers.ParsingHelpers.PROTOCOLS: [],
            helpers.ParsingHelpers.STRUCTS: [],
            helpers.ParsingHelpers.CLASSES: [],
            helpers.ParsingHelpers.FUNCS: [],
        }

    def parse(self):
        n_of_comments = 0
        loc = 0

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
                    if not commented_line:
                        n_of_comments += 1
                    commented_line = False
                    continue

                if commented_line:
                    n_of_comments += 1
                    continue

                loc += 1

                for key, value in self.attributes_regex_map.items():
                    extracted_value = helpers.ParsingHelpers.extract_substring_with_pattern(key, trimmed)
                    if len(extracted_value) > 0:
                        value.append(extracted_value)
                        continue

        return SwiftFile(
            framework_name=self.__framework_name(),
            loc=loc,
            imports=self.attributes_regex_map[helpers.ParsingHelpers.IMPORTS],
            interfaces=self.attributes_regex_map[helpers.ParsingHelpers.PROTOCOLS],
            structs=self.attributes_regex_map[helpers.ParsingHelpers.STRUCTS],
            classes=self.attributes_regex_map[helpers.ParsingHelpers.CLASSES],
            methods=self.attributes_regex_map[helpers.ParsingHelpers.FUNCS],
            n_of_comments=n_of_comments
        )

    # Private helpers

    def __framework_name(self):
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath(subdir)
        if first_subpath.endswith('.swift'):
            return 'AppTarget'
        else:
            return first_subpath

    def __extract_first_subpath(self, subdir):
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath(subdirs[0])
        else:
            return subdir.replace('/', '')
