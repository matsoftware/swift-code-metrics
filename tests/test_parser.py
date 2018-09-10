import unittest
from swift_code_metrics import _parser


class ParserTests(unittest.TestCase):

    def setUp(self):
        self.example_parsed_file = _parser.SwiftFileParser(
            file="test_resources/ExampleFile.swift",
            base_path=""
        ).parse()

    def test_swiftparser_parse_should_return_expected_framework_name(self):
        self.assertEqual(self.example_parsed_file.framework_name, "test_resources")

    def test_swiftparser_parse_should_return_expected_n_of_comments(self):
        self.assertEqual(21, self.example_parsed_file.n_of_comments)

    def test_swiftparser_parse_should_return_expected_loc(self):
        self.assertEqual(23, self.example_parsed_file.loc)

    def test_swiftparser_parse_should_return_expected_imports(self):
        self.assertEqual(['Foundation', 'AmazingFramework'], self.example_parsed_file.imports)

    def test_swiftparser_parse_should_return_expected_interfaces(self):
        self.assertEqual(['SimpleProtocol', 'UnusedClassProtocol'], self.example_parsed_file.interfaces)

    def test_swiftparser_parse_should_return_expected_structs(self):
        self.assertEqual(['GenericStruct<T>', 'InternalStruct'], self.example_parsed_file.structs)

    def test_swiftparser_parse_should_return_expected_classes(self):
        self.assertEqual(['SimpleClass',
                          'ComplexClass',
                          'ComposedAttributedClass',
                          'ComposedPrivateClass'], self.example_parsed_file.classes)

    def test_swiftparser_parse_should_return_expected_methods(self):
        self.assertEqual(['methodOne',
                          'methodTwo',
                          'privateFunction',
                          'aStaticMethod'], self.example_parsed_file.methods)

if __name__ == '__main__':
    unittest.main()
