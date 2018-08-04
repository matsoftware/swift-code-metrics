import unittest
import parser
import helpers


class HelpersTests(unittest.TestCase):

    #  Comments

    def test_helpers_begin_comment_check_existence_expectedFalse(self):
        regex = helpers.ParsingHelpers.BEGIN_COMMENT
        string = ' Comment /* fake comment */'
        self.assertFalse(helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_begin_comment_check_existence_expectedTrue(self):
        regex = helpers.ParsingHelpers.BEGIN_COMMENT
        string = '/* True comment */'
        self.assertTrue(helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_end_comment_check_existence_expectedFalse(self):
        regex = helpers.ParsingHelpers.END_COMMENT
        string = ' Fake comment */ ending'
        self.assertFalse(helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_end_comment_check_existence_expectedTrue(self):
        regex = helpers.ParsingHelpers.END_COMMENT
        string = ' True comment ending */'
        self.assertTrue(helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_single_comment_check_existence_expectedFalse(self):
        regex = helpers.ParsingHelpers.SINGLE_COMMENT
        string = 'Fake single // comment //'
        self.assertFalse(helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_single_comment_check_existence_expectedTrue(self):
        regex = helpers.ParsingHelpers.SINGLE_COMMENT
        string = '// True single line comment'
        self.assertTrue(helpers.ParsingHelpers.check_existence(regex, string))


    # Imports

    def test_helpers_imports_extract_substring_with_pattern_expectFalse(self):
        regex = helpers.ParsingHelpers.IMPORTS
        string = '//import Foundation '
        self.assertEqual('', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.IMPORTS
        string = 'import Foundation'
        self.assertEqual('Foundation', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Protocols

    def test_helpers_protocols_extract_substring_with_pattern_expectFalse(self):
        regex = helpers.ParsingHelpers.PROTOCOLS
        string = 'class Conformstoprotocol: Any '
        self.assertEqual('', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_space_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.PROTOCOLS
        string = 'protocol Any : class'
        self.assertEqual('Any', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_colons_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.PROTOCOLS
        string = 'protocol Any: class'
        self.assertEqual('Any', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.PROTOCOLS
        string = 'public protocol Pubblico {}'
        self.assertEqual('Pubblico', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

if __name__ == '__main__':
    unittest.main()
