import unittest
import os
import sys
from swift_code_metrics import scm
from swift_code_metrics._helpers import JSONReader


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        sys.argv.clear()
        sys.argv.append(os.path.dirname(os.path.realpath(__file__)))
        sys.argv.append("--source")
        sys.argv.append("swift_code_metrics/tests/test_resources/ExampleProject/SwiftCodeMetricsExample")
        sys.argv.append("--artifacts")
        sys.argv.append("swift_code_metrics/tests/report")
        sys.argv.append("--generate-graphs")

    def tearDown(self):
        sys.argv.clear()

    def test_sample_app(self):
        output_file = "swift_code_metrics/tests/report/output.json"
        scm.main()  # generate report
        expected_file = os.path.join("swift_code_metrics/tests/test_resources", "expected_output.json")
        expected_json = JSONReader.read_json_file(expected_file)
        generated_json = JSONReader.read_json_file(output_file)
        self.assertEqual(generated_json, expected_json)


class IntegrationUnhappyTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        sys.argv.clear()
        sys.argv.append(os.path.dirname(os.path.realpath(__file__)))
        sys.argv.append("--source")
        sys.argv.append("any")
        sys.argv.append("--artifacts")
        sys.argv.append("any")

    def tearDown(self):
        sys.argv.clear()

    def test_sample_app(self):
        with self.assertRaises(SystemExit) as cm:
            scm.main()  # should not throw exception and return 0

        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
