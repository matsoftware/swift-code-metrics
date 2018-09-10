import unittest
import os
import filecmp
import sys
from swift_code_metrics import scm


class IntegrationTest(unittest.TestCase):
    def test_sample_app(self):
        sys.argv.append("--source")
        sys.argv.append("test_resources/ExampleProject/SwiftCodeMetricsExample")
        sys.argv.append("--artifacts")
        sys.argv.append("report")
        sys.argv.append("--generate-graphs")
        output_file = "../report/output.json"
        scm.main()
        expected_file = os.path.join("test_resources", "expected_output.json")
        self.assertTrue(filecmp.cmp(expected_file, output_file, shallow=False))


if __name__ == '__main__':
    unittest.main()
