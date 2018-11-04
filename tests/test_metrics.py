import unittest
from swift_code_metrics._metrics import Framework, Dependency
from swift_code_metrics._metrics import Metrics


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
        for sf in MetricsTests.__dummy_external_frameworks():
            self.foundation_kit.append_import(sf)

        foundation_external_deps = Metrics.external_dependencies(self.foundation_kit, self.frameworks)
        expected_external_deps = [Dependency('FoundationKit', 'AwesomeDependency', 1),
                                  Dependency('FoundationKit', 'RxSwift', 1)]

        design_external_deps = Metrics.external_dependencies(self.design_kit, self.frameworks)

        self.assertEqual(expected_external_deps, foundation_external_deps)
        self.assertEqual(design_external_deps, [])

    def test_internal_dependencies(self):
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.foundation_kit)
        self.design_kit.append_import(self.foundation_kit)

        expected_foundation_internal_deps = []
        expected_design_internal_deps = [Dependency('DesignKit', 'FoundationKit', 1)]
        expected_app_layer_internal_deps = [Dependency('ApplicationLayer', 'DesignKit', 2),
                                            Dependency('ApplicationLayer', 'FoundationKit', 1)]

        self.assertEqual(expected_foundation_internal_deps,
                         Metrics.internal_dependencies(self.foundation_kit, self.frameworks))
        self.assertEqual(expected_design_internal_deps,
                         Metrics.internal_dependencies(self.design_kit, self.frameworks))
        self.assertEqual(expected_app_layer_internal_deps,
                         Metrics.internal_dependencies(self.app_layer, self.frameworks))

    @staticmethod
    def __dummy_external_frameworks():
        return [
            Framework('Foundation'),
            Framework('UIKit'),
            Framework('RxSwift'),
            Framework('AwesomeDependency')
        ]


if __name__ == '__main__':
    unittest.main()
