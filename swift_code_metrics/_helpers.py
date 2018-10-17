import re


class AnalyzerHelpers:

    # Constants

    SWIFT_FILE_EXTENSION = '.swift'

    @staticmethod
    def is_path_in_list(subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False


class ParsingHelpers:

    # Constants

    DEFAULT_FRAMEWORK_NAME = 'AppTarget'
    DEFAULT_TEST_FRAMEWORK_SUFFIX = '_Test'
    TEST_METHOD_PREFIX = 'test'

    # Constants - Regex patterns

    BEGIN_COMMENT = '^//*'
    END_COMMENT = '\*/$'
    SINGLE_COMMENT = '^//'

    IMPORTS = '^import (.*?)$'

    PROTOCOLS = '.*protocol (.*?)[:|{|\s]'
    STRUCTS = '.*struct (.*?)[:|{|\s]'
    CLASSES = '.*class (.*?)[:|{|\s]'
    FUNCS = '.*func (.*?)[:|\(|\s]'

    # Static helpers

    @staticmethod
    def check_existence(regex_pattern, trimmed_string):
        regex = re.compile(regex_pattern)
        if re.search(regex, trimmed_string.strip()) is not None:
            return True
        else:
            return False

    @staticmethod
    def extract_substring_with_pattern(regex_pattern, trimmed_string):
        try:
            return re.search(regex_pattern, trimmed_string).group(1)
        except AttributeError:
            return ''


class ReportingHelpers:

    @staticmethod
    def decimal_format(number, decimal_places=3):
        format_string = "{:." + str(decimal_places) + "f}"
        return float(format_string.format(number))
