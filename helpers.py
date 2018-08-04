import re


class ParsingHelpers:
    # constants
    BEGIN_COMMENT = '^//*'
    END_COMMENT = '\*/$'
    SINGLE_COMMENT = '^//'

    # Static helpers

    @staticmethod
    def check_existence(regex_pattern, trimming_string):
        regex = re.compile(regex_pattern)
        if re.search(regex, trimming_string.strip()) is not None:
            return True
        else:
            return False