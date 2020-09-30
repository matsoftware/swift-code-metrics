import unittest
from swift_code_metrics import _helpers


class HelpersTests(unittest.TestCase):

    #  Comments

    def test_helpers_begin_comment_check_existence_expectedFalse(self):
        regex = _helpers.ParsingHelpers.BEGIN_COMMENT
        string = ' Comment /* fake comment */'
        self.assertFalse(_helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_begin_comment_check_existence_expectedTrue(self):
        regex = _helpers.ParsingHelpers.BEGIN_COMMENT
        string = '/* True comment */'
        self.assertTrue(_helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_end_comment_check_existence_expectedFalse(self):
        regex = _helpers.ParsingHelpers.END_COMMENT
        string = ' Fake comment */ ending'
        self.assertFalse(_helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_end_comment_check_existence_expectedTrue(self):
        regex = _helpers.ParsingHelpers.END_COMMENT
        string = ' True comment ending */'
        self.assertTrue(_helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_single_comment_check_existence_expectedFalse(self):
        regex = _helpers.ParsingHelpers.SINGLE_COMMENT
        string = 'Fake single // comment //'
        self.assertFalse(_helpers.ParsingHelpers.check_existence(regex, string))

    def test_helpers_single_comment_check_existence_expectedTrue(self):
        regex = _helpers.ParsingHelpers.SINGLE_COMMENT
        string = '// True single line comment'
        self.assertTrue(_helpers.ParsingHelpers.check_existence(regex, string))

    # Imports

    def test_helpers_imports_extract_substring_with_pattern_expectFalse(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = '//import Foundation '
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_leading_semicolon_expectFalse(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'import Foundation;'
        self.assertEqual('Foundation', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'import Foundation '
        self.assertEqual('Foundation', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_submodule_expectTrue(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'import Foundation.KeyChain'
        self.assertEqual('Foundation', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_subcomponent_expectTrue(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'import struct Foundation.KeyChain'
        self.assertEqual('Foundation', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_comments_expectTrue(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'import Contacts // fix for `dyld: Library not loaded: @rpath/libswiftContacts.dylib`'
        self.assertEqual('Contacts', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_imports_specialwords_expectFalse(self):
        regex = _helpers.ParsingHelpers.IMPORTS
        string = 'importedMigratedComponents: AnyImportedComponent'
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Protocols

    def test_helpers_protocols_extract_substring_with_pattern_expectFalse(self):
        regex = _helpers.ParsingHelpers.PROTOCOLS
        string = 'class Conformstoprotocol: Any '
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_space_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.PROTOCOLS
        string = 'protocol Any : class'
        self.assertEqual('Any', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_colons_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.PROTOCOLS
        string = 'protocol Any: class'
        self.assertEqual('Any', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_protocols_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.PROTOCOLS
        string = 'public protocol Pubblico{}'
        self.assertEqual('Pubblico', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Structs

    def test_helpers_structs_extract_substring_with_pattern_expectFalse(self):
        regex = _helpers.ParsingHelpers.STRUCTS
        string = 'class Fakestruct: Any '
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_space_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.STRUCTS
        string = 'struct AnyStruct : Protocol {'
        self.assertEqual('AnyStruct', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_colons_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.STRUCTS
        string = 'struct AnyStruct {}'
        self.assertEqual('AnyStruct', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_structs_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.STRUCTS
        string = 'internal struct Internal{'
        self.assertEqual('Internal', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Class

    def test_helpers_class_extract_substring_with_pattern_expectFalse(self):
        regex = _helpers.ParsingHelpers.CLASSES
        string = 'struct Fakeclass: Any '
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_space_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.CLASSES
        string = 'class MyClass : Protocol {'
        self.assertEqual('MyClass', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_colons_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.CLASSES
        string = 'class MyClass {}'
        self.assertEqual('MyClass', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_class_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.CLASSES
        string = 'private class Private{'
        self.assertEqual('Private', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    # Funcs

    def test_helpers_funcs_extract_substring_with_pattern_expectFalse(self):
        regex = _helpers.ParsingHelpers.FUNCS
        string = 'struct Fakefunc: Any '
        self.assertEqual('', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_funcs_space_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.FUNCS
        string = 'func myFunction() -> Bool {'
        self.assertEqual('myFunction', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_funcs_parameters_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.FUNCS
        string = 'func myFunction(with parameter: String) '
        self.assertEqual('myFunction', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_funcs_property_modifier_extract_substring_with_pattern_expectTrue(self):
        regex = _helpers.ParsingHelpers.FUNCS
        string = 'private func funzione(){'
        self.assertEqual('funzione', _helpers.ParsingHelpers.extract_substring_with_pattern(regex, string))

    def test_helpers_funcs_reduce_dictionary(self):
        self.assertEqual(3, _helpers.ParsingHelpers.reduce_dictionary({"one": 1, "two": 2}))


if __name__ == '__main__':
    unittest.main()
