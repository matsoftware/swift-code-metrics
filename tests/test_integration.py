import unittest
import os
import filecmp
import sys
from swift_code_metrics import scm


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        sys.argv.clear()
        sys.argv.append(os.path.dirname(os.path.realpath(__file__)))
        sys.argv.append("--source")
        sys.argv.append("test_resources/ExampleProject/SwiftCodeMetricsExample")
        sys.argv.append("--artifacts")
        sys.argv.append("report")
        sys.argv.append("--exclude")
        sys.argv.append("Tests")
        sys.argv.append("--generate-graphs")

    def tearDown(self):
        sys.argv.clear()

    def test_sample_app(self):
        output_file = "report/output.json"
        scm.main()
        expected_file = os.path.join("test_resources", "expected_output.json")
        self.assertTrue(filecmp.cmp(expected_file, output_file, shallow=False))


if __name__ == '__main__':
    unittest.main()
