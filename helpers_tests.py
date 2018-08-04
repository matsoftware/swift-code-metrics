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
        string = 'public protocol Pubblico{}'
        self.assertEqual('Pubblico', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Structs

    def test_helpers_structs_extract_substring_with_pattern_expectFalse(self):
        regex = helpers.ParsingHelpers.STRUCTS
        string = 'class Fakestruct: Any '
        self.assertEqual('', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_space_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.STRUCTS
        string = 'struct AnyStruct : Protocol {'
        self.assertEqual('AnyStruct', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_colons_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.STRUCTS
        string = 'struct AnyStruct {}'
        self.assertEqual('AnyStruct', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.STRUCTS
        string = 'internal struct Internal{'
        self.assertEqual('Internal', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Class

    def test_helpers_class_extract_substring_with_pattern_expectFalse(self):
        regex = helpers.ParsingHelpers.CLASSES
        string = 'struct Fakeclass: Any '
        self.assertEqual('', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_space_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.CLASSES
        string = 'class MyClass : Protocol {'
        self.assertEqual('MyClass', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_colons_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.CLASSES
        string = 'class MyClass {}'
        self.assertEqual('MyClass', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = helpers.ParsingHelpers.CLASSES
        string = 'private class Private{'
        self.assertEqual('Private', helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

if __name__ == '__main__':
    unittest.main()
