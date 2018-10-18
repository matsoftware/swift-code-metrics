import unittest
from swift_code_metrics import _metrics


class FrameworkTests(unittest.TestCase):

    def setUp(self):
        self.dummy_framework = _metrics.Framework('AwesomeName')

    def test_compact_name(self):
        self.assertEqual(self.dummy_framework.compact_name, 'AN')

    def test_compact_name_description(self):
        self.assertEqual(self.dummy_framework.compact_name_description, 'AN = AwesomeName')


if __name__ == '__main__':
    unittest.main()
