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



if __name__ == '__main__':
    unittest.main()
