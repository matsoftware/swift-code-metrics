import unittest
from swift_code_metrics._metrics import Framework, Dependency, Metrics, SyntheticData, FrameworkData
from swift_code_metrics._parser import SwiftFile
from functional import seq

example_swiftfile = SwiftFile(
    framework_name=['Test'],
    loc=1,
    imports=['dep1', 'dep2'],
    interfaces=['prot1', 'prot2', 'prot3'],
    structs=['struct'],
    classes=['class'],
    methods=['meth1', 'meth2', 'meth3', 'testMethod'],
    n_of_comments=7,
    is_shared=True,
    is_test=False
)


class FrameworkTests(unittest.TestCase):

    def setUp(self):
        self.frameworks = [Framework('BusinessLogic'), Framework('UIKit'), Framework('Other')]
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

    def _populate_app_layer_imports(self):
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.foundation_kit)

    def test_distance_main_sequence(self):
        self._populate_app_layer_imports()
        self.app_layer.data.number_of_concrete_data_structures = 7
        self.app_layer.data.number_of_interfaces = 2

        self.assertAlmostEqual(0.286,
                               Metrics.distance_main_sequence(self.app_layer, self.frameworks),
                               places=3)

    def test_instability_no_imports(self):
        self.assertEqual(0, Metrics.instability(self.foundation_kit, self.frameworks))

    def test_instability_imports(self):
        self._populate_app_layer_imports()
        self.assertAlmostEqual(1.0, Metrics.instability(self.app_layer, self.frameworks))

    def test_abstractness_no_concretes(self):
        self.assertEqual(0, Metrics.abstractness(self.foundation_kit))

    def test_abstractness_concretes(self):
        self.foundation_kit.data.number_of_interfaces = 8
        self.foundation_kit.data.number_of_concrete_data_structures = 4
        self.assertEqual(2, Metrics.abstractness(self.foundation_kit))

    def test_fan_in(self):
        self._populate_app_layer_imports()
        self.assertEqual(2, Metrics.fan_in(self.design_kit, self.frameworks))

    def test_fan_out(self):
        self._populate_app_layer_imports()
        self.assertEqual(3, Metrics.fan_out(self.app_layer))

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
        self._populate_app_layer_imports()
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

    def test_poc_valid_loc_noc(self):
        self.assertEqual(50, Metrics.percentage_of_comments(loc=2, noc=2))

    def test_poc_invalid_loc_noc(self):
        self.assertEqual(0, Metrics.percentage_of_comments(loc=0, noc=0))

    @property
    def __dummy_external_frameworks(self):
        return [
            Framework('Foundation'),
            Framework('UIKit'),
            self.rxswift,
            self.awesome_dependency,
        ]


class SyntheticDataTests(unittest.TestCase):

    def setUp(self):
        self.synthetic_data = SyntheticData(swift_file=example_swiftfile)

    def test_init_no_swift_file(self):
        empty_data = SyntheticData()
        self.assertEqual(0, empty_data.loc)
        self.assertEqual(0, empty_data.noc)
        self.assertEqual(0, empty_data.number_of_concrete_data_structures)
        self.assertEqual(0, empty_data.number_of_interfaces)
        self.assertEqual(0, empty_data.number_of_methods)
        self.assertEqual(0, empty_data.number_of_tests)

    def test_synthetic_init_swiftfile(self):
        self.assertEqual(1, self.synthetic_data.loc)
        self.assertEqual(7, self.synthetic_data.noc)
        self.assertEqual(2, self.synthetic_data.number_of_concrete_data_structures)
        self.assertEqual(3, self.synthetic_data.number_of_interfaces)
        self.assertEqual(4, self.synthetic_data.number_of_methods)
        self.assertEqual(1, self.synthetic_data.number_of_tests)

    def test_append_data(self):
        additional_data = SyntheticData(swift_file=example_swiftfile)
        self.synthetic_data.append_data(data=additional_data)
        self.assertEqual(2, self.synthetic_data.loc)
        self.assertEqual(14, self.synthetic_data.noc)
        self.assertEqual(4, self.synthetic_data.number_of_concrete_data_structures)
        self.assertEqual(6, self.synthetic_data.number_of_interfaces)
        self.assertEqual(8, self.synthetic_data.number_of_methods)
        self.assertEqual(2, self.synthetic_data.number_of_tests)

    def test_poc(self):
        self.assertAlmostEqual(87.5, self.synthetic_data.poc)

    def test_as_dict(self):
        expected_dict = {
            "loc": 1,
            "noc": 7,
            "n_a": 3,
            "n_c": 2,
            "nom": 4,
            "not": 1,
            "poc": 87.5
        }
        self.assertEqual(expected_dict, self.synthetic_data.as_dict)


class FrameworkDataTests(unittest.TestCase):

    def setUp(self):
        self.framework_data = FrameworkData(swift_file=example_swiftfile)

    def test_init_no_swift_file(self):
        self.assertEqual(1, self.framework_data.loc)
        self.assertEqual(7, self.framework_data.noc)
        self.assertEqual(2, self.framework_data.number_of_concrete_data_structures)
        self.assertEqual(3, self.framework_data.number_of_interfaces)
        self.assertEqual(4, self.framework_data.number_of_methods)
        self.assertEqual(1, self.framework_data.number_of_tests)
        self.assertEqual(0, self.framework_data.n_o_i)

    def test_append_framework(self):
        framework_additional_data = SyntheticData(swift_file=example_swiftfile)
        test_framework = Framework('Test')
        test_framework.append_import(Framework('Imported'))
        test_framework.data = framework_additional_data

        self.framework_data.append_framework(test_framework)
        self.assertEqual(2, self.framework_data.loc)
        self.assertEqual(14, self.framework_data.noc)
        self.assertEqual(4, self.framework_data.number_of_concrete_data_structures)
        self.assertEqual(6, self.framework_data.number_of_interfaces)
        self.assertEqual(8, self.framework_data.number_of_methods)
        self.assertEqual(2, self.framework_data.number_of_tests)
        self.assertEqual(1, self.framework_data.n_o_i)

    def test_as_dict(self):
        expected_dict = {
            "loc": 1,
            "noc": 7,
            "n_a": 3,
            "n_c": 2,
            "nom": 4,
            "not": 1,
            "poc": 87.5,
            "noi": 0
        }
        self.assertEqual(expected_dict, self.framework_data.as_dict)


if __name__ == '__main__':
    unittest.main()
