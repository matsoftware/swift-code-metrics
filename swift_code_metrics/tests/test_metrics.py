import unittest
from swift_code_metrics._metrics import Framework, Dependency
from swift_code_metrics._metrics import Metrics
from functional import seq


class FrameworkTests(unittest.TestCase):

    def setUp(self):
        self.frameworks = [Framework('BusinessLogic'), Framework('UIKit'), Framework('Other'), ]
        self.framework = Framework('AwesomeName')
        seq(self.frameworks) \
            .for_each(lambda f: self.framework.append_import(f))

    def test_representation(self):
        self.assertEqual(str(self.framework), 'AwesomeName(0 files)')

    def test_compact_name_morethanfourcapitals(self):
        test_framework = Framework('FrameworkWithMoreThanFourCapitals')
        self.assertEqual('FC', test_framework.compact_name)

    def test_compact_name_lessthanfourcapitals(self):
        self.assertEqual('AN', self.framework.compact_name)

    def test_compact_name_nocapitals(self):
        test_framework = Framework('nocapitals')
        self.assertEqual('n', test_framework.compact_name)

    def test_compact_name_description(self):
        self.assertEqual(self.framework.compact_name_description, 'AN = AwesomeName')

    def test_imports(self):
        expected_imports = {self.frameworks[0]: 1,
                            self.frameworks[2]: 1}
        self.assertEqual(expected_imports, self.framework.imports)

    def test_number_of_imports(self):
        self.assertEqual(2, self.framework.number_of_imports)


class DependencyTests(unittest.TestCase):

    def setUp(self):
        self.dependency = Dependency('AppLayer', 'DesignKit', 2)

    def test_repr(self):
        self.assertEqual('AppLayer - DesignKit (2) imports', str(self.dependency))

    def test_compact_repr(self):
        self.assertEqual('AppLayer (2)', self.dependency.compact_repr)

    def test_relation(self):
        self.assertEqual('AppLayer > DesignKit', self.dependency.relationship)


class MetricsTests(unittest.TestCase):

    def setUp(self):
        self._generate_mocks()

    def _generate_mocks(self):
        self.foundation_kit = Framework('FoundationKit')
        self.design_kit = Framework('DesignKit')
        self.app_layer = Framework('ApplicationLayer')
        self.rxswift = Framework('RxSwift')
        self.awesome_dependency = Framework('AwesomeDependency')
        self.frameworks = [
            self.foundation_kit,
            self.design_kit,
            self.app_layer
        ]

    def test_external_dependencies(self):
        for sf in self.__dummy_external_frameworks:
            self.foundation_kit.append_import(sf)

        foundation_external_deps = Metrics.external_dependencies(self.foundation_kit, self.frameworks)
        expected_external_deps = [Dependency('FoundationKit', 'RxSwift', 1),
                                  Dependency('FoundationKit', 'AwesomeDependency', 1)]

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

    def test_total_dependencies(self):
        for sf in self.__dummy_external_frameworks:
            self.foundation_kit.append_import(sf)
        self.foundation_kit.append_import(self.design_kit)

        expected_deps = ['RxSwift(1)', 'AwesomeDependency(1)', 'DesignKit(1)']

        self.assertEqual(expected_deps,
                         Metrics.total_dependencies(self.foundation_kit))

    @property
    def __dummy_external_frameworks(self):
        return [
            Framework('Foundation'),
            Framework('UIKit'),
            self.rxswift,
            self.awesome_dependency,
        ]


if __name__ == '__main__':
    unittest.main()
