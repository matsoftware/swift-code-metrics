import re


class ParsingHelpers:

    # Constants

    BEGIN_COMMENT = '^//*'
    END_COMMENT = '\*/$'
    SINGLE_COMMENT = '^//'

    IMPORTS = '^import (.*?)$'
    PROTOCOLS = '.*protocol (.*?)[:|{|\s]'
    STRUCTS = '.*struct (.*?)[:|{|\s]'
    CLASSES = '.*class (.*?)[:|{|\s]'

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