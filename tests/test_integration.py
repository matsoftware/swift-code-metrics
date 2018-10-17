import unittest
import os
import sys
from swift_code_metrics import scm
import json


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
        scm.main()  # generate report
        expected_file = os.path.join("test_resources", "expected_output.json")
        expected_json = IntegrationTest.read_json_file(expected_file)
        generated_json = IntegrationTest.read_json_file(output_file)
        self.assertEqual(generated_json, expected_json)


    @staticmethod
    def read_json_file(path):
        with open(path, 'r') as fp:
            return json.load(fp)


if __name__ == '__main__':
    unittest.main()
