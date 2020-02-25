import unittest
from swift_code_metrics._parser import SwiftFileParser, ProjectPathsOverride
from json import JSONDecodeError


class ParserTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ParserTests, self).__init__(*args, **kwargs)
        self._generate_mocks()

    def _generate_mocks(self):
        self.example_parsed_file = SwiftFileParser(
            file="swift_code_metrics/tests/test_resources/ExampleFile.swift",
            base_path="swift_code_metrics/tests",
            current_subdir="tests",
            tests_default_paths=""
        ).parse()[0]
        self.example_test_file = SwiftFileParser(
            file="swift_code_metrics/tests/test_resources/ExampleTest.swift",
            base_path="swift_code_metrics/tests",
            current_subdir="swift_code_metrics",
            tests_default_paths="Test"
        ).parse()[0]

    # Non-test file

    def test_swiftparser_parse_should_return_expected_framework_name(self):
        self.assertEqual(self.example_parsed_file.framework_name, "test_resources")

    def test_swiftparser_parse_should_return_expected_n_of_comments(self):
        self.assertEqual(21, self.example_parsed_file.n_of_comments)

    def test_swiftparser_parse_should_return_expected_loc(self):
        self.assertEqual(25, self.example_parsed_file.loc)

    def test_swiftparser_parse_should_return_expected_imports(self):
        self.assertEqual(['Foundation', 'AmazingFramework', 'Helper', 'TestedLibrary'], self.example_parsed_file.imports)

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

    # Test file

    def test_swiftparser_parse_test_file_shouldAppendSuffixFrameworkName(self):
        self.assertEqual(self.example_test_file.framework_name, "test_resources_Test")

    def test_swiftfile_noTestClass_numberOfTests_shouldReturnExpectedNumber(self):
        self.assertEqual(len(self.example_parsed_file.tests), 0)

    def test_swiftfile_testClass_numberOfTests_shouldReturnExpectedNumber(self):
        self.assertEqual(len(self.example_test_file.methods), 3)
        self.assertEqual(['test_example_assertion',
                          'testAnotherExample'], self.example_test_file.tests)


class ProjectPathsOverrideTests(unittest.TestCase):

    def test_projectpathsoverride_loadFromJson_validfile_shouldParseExpectedData(self):
        path = "swift_code_metrics/tests/test_resources/scm_overrides/valid_scm_override.json"
        path_override = ProjectPathsOverride.load_from_json(path)
        expected_path_override = ProjectPathsOverride(entries={
            "libraries": [
                {
                    "name": "FoundationFramework",
                    "path": "FoundationFramework",
                    "is_test": False
                },
                {
                    "name": "FoundationFrameworkTests",
                    "path": "FoundationFrameworkTests",
                    "is_test": True
                },
                {
                    "name": "SecretLib",
                    "path": "SecretLib",
                    "is_test": False
                }
            ],
            "shared": [
                {
                    "path": "Shared",
                    "is_test": False
                }
            ]
        })
        self.assertEqual(path_override, expected_path_override)

    def test_projectpathsoverride_loadFromJson_invalidfile_shouldRaiseException(self):
        path = "swift_code_metrics/tests/test_resources/scm_overrides/invalid_scm_override.json"
        with self.assertRaises(JSONDecodeError) as cm:
            ProjectPathsOverride.load_from_json(path)

        self.assertIsNotNone(cm)


if __name__ == '__main__':
    unittest.main()
