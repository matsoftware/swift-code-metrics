import unittest
from swift_code_metrics import _analyzer
import filecmp
import os


class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.analyzer = _analyzer.Inspector(
            directory="test_resources/ExampleProject/SwiftCodeMetricsExample",
            exclude_paths=["Test"],
            artifacts="."
        )

    def test_inspector_generated_output(self):
        output_file = "output.json"
        expected_file = os.path.join("test_resources", "expected_output.json")
        self.assertTrue(filecmp.cmp(expected_file, output_file, shallow=False))
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
