import unittest
from swift_code_metrics._metrics import Framework
from swift_code_metrics._metrics import Metrics
from tests import dummies


class FrameworkTests(unittest.TestCase):

    def setUp(self):
        self.dummy_framework = Framework('AwesomeName')

    def test_compact_name(self):
        self.assertEqual(self.dummy_framework.compact_name, 'AN')

    def test_compact_name_description(self):
        self.assertEqual(self.dummy_framework.compact_name_description, 'AN = AwesomeName')


class MetricsTests(unittest.TestCase):

    def setUp(self):
        self._generate_mocks()

    def _generate_mocks(self):
        self.foundation_kit = Framework('FoundationKit')
        self.design_kit = Framework('DesignKit')
        self.app_layer = Framework('ApplicationLayer')
        self.frameworks = [
            self.foundation_kit,
            self.design_kit,
            self.app_layer
        ]

    def test_external_dependencies(self):
        for sf in dummies.dummy_external_frameworks():
            self.foundation_kit.append_import(sf)

        foundation_external_deps = Metrics.external_dependencies(self.foundation_kit, self.frameworks)
        design_external_deps = Metrics.external_dependencies(self.design_kit, self.frameworks)

        self.assertEqual(MetricsTests.__extract_names(foundation_external_deps),
                         MetricsTests.__extract_names(dummies.dummy_external_frameworks()))
        self.assertEqual(MetricsTests.__extract_names(design_external_deps), [])



    @staticmethod
    def __extract_names(frameworks):
        return list(map(lambda f: f.name, frameworks))


if __name__ == '__main__':
    unittest.main()
