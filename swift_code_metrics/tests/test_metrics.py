import unittest
from swift_code_metrics._metrics import Framework, Dependency, Metrics, SyntheticData, FrameworkData, SubModule
from swift_code_metrics._parser import SwiftFile
from functional import seq

example_swiftfile = SwiftFile(
    path='/my/path/class.swift',
    framework_name='Test',
    loc=1,
    imports=['Foundation', 'dep1', 'dep2'],
    interfaces=['prot1', 'prot2', 'prot3'],
    structs=['struct'],
    classes=['class'],
    methods=['meth1', 'meth2', 'meth3', 'testMethod'],
    n_of_comments=7,
    is_shared=True,
    is_test=False
)

example_file2 = SwiftFile(
            path='/my/path/class.swift',
            framework_name='Test',
            loc=1,
            imports=['Foundation', 'dep1', 'dep2'],
            interfaces=['prot1', 'prot2', 'prot3', 'prot4',
                        'prot5', 'prot6', 'prot7', 'prot8'],
            structs=['struct1', 'struct2'],
            classes=['class1', 'class2'],
            methods=['meth1', 'meth2', 'meth3', 'testMethod'],
            n_of_comments=7,
            is_shared=False,
            is_test=False
        )


class FrameworkTests(unittest.TestCase):

    def setUp(self):
        self.frameworks = [Framework('BusinessLogic'), Framework('UIKit'), Framework('Other')]
        self.framework = Framework('AwesomeName')
        self.framework.submodule.files = [example_swiftfile, example_file2]
        seq(self.frameworks) \
            .for_each(lambda f: self.framework.append_import(f))

    def test_representation(self):
        self.assertEqual('AwesomeName(2 files)', str(self.framework))

    def test_compact_name_more_than_four_capitals(self):
        test_framework = Framework('FrameworkWithMoreThanFourCapitals')
        self.assertEqual('FC', test_framework.compact_name)

    def test_compact_name_less_than_four_capitals(self):
        self.assertEqual('AN', self.framework.compact_name)

    def test_compact_name_no_capitals(self):
        test_framework = Framework('nocapitals')
        self.assertEqual('n', test_framework.compact_name)

    def test_compact_name_description(self):
        self.assertEqual('AN = AwesomeName', self.framework.compact_name_description)

    def test_imports(self):
        expected_imports = {self.frameworks[0]: 1,
                            self.frameworks[2]: 1}
        self.assertEqual(expected_imports, self.framework.imports)

    def test_number_of_imports(self):
        self.assertEqual(2, self.framework.number_of_imports)

    def test_number_of_files(self):
        self.assertEqual(2, self.framework.number_of_files)

    def test_synthetic_data(self):
        self.assertEqual(self.framework.data.loc, 2)
        self.assertEqual(self.framework.data.noc, 14)


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
        self._populate_imports()

    def _generate_mocks(self):
        self.foundation_kit = Framework('FoundationKit')
        self.design_kit = Framework('DesignKit')
        self.app_layer = Framework('ApplicationLayer')
        self.rxswift = Framework('RxSwift')
        self.test_design_kit = Framework(name='DesignKitTests', is_test_framework=True)
        self.awesome_dependency = Framework('AwesomeDependency')
        self.not_linked_framework = Framework('External')
        self.frameworks = [
            self.foundation_kit,
            self.design_kit,
            self.app_layer,
            self.test_design_kit
        ]

    def _populate_imports(self):
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.design_kit)
        self.app_layer.append_import(self.foundation_kit)
        self.test_design_kit.append_import(self.design_kit)

    def test_distance_main_sequence(self):

        example_file = SwiftFile(
            path='/my/path/class.swift',
            framework_name='Test',
            loc=1,
            imports=['Foundation', 'dep1', 'dep2'],
            interfaces=['prot1', 'prot2'],
            structs=['struct1', 'struct2', 'struct3', 'struct4'],
            classes=['class1', 'class2', 'class3'],
            methods=['meth1', 'meth2', 'meth3', 'testMethod'],
            n_of_comments=7,
            is_shared=False,
            is_test=False
        )
        self.app_layer.submodule.files.append(example_file)

        self.assertAlmostEqual(0.286,
                               Metrics.distance_main_sequence(self.app_layer, self.frameworks),
                               places=3)

    def test_instability_no_imports(self):
        self.assertEqual(0, Metrics.instability(self.foundation_kit, self.frameworks))

    def test_instability_not_linked_framework(self):
        self.assertEqual(0, Metrics.instability(self.not_linked_framework, self.frameworks))

    def test_instability_imports(self):
        self.assertAlmostEqual(1.0, Metrics.instability(self.app_layer, self.frameworks))

    def test_abstractness_no_concretes(self):
        self.assertEqual(0, Metrics.abstractness(self.foundation_kit))

    def test_abstractness_concretes(self):
        self.foundation_kit.submodule.files.append(example_file2)
        self.assertEqual(2, Metrics.abstractness(self.foundation_kit))

    def test_fan_in_test_frameworks(self):
        self.assertEqual(2, Metrics.fan_in(self.design_kit, self.frameworks))

    def test_fan_in_no_test_frameworks(self):
        self.assertEqual(1, Metrics.fan_in(self.foundation_kit, self.frameworks))

    def test_fan_out(self):
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

    def test_ia_analysis_zone_of_pain(self):
        self.assertTrue("Zone of Pain" in Metrics.ia_analysis(0.4, 0.4))

    def test_ia_analysis_zone_of_uselessness(self):
        self.assertTrue("Zone of Uselessness" in Metrics.ia_analysis(0.7, 0.7))

    def test_ia_analysis_highly_stable(self):
        self.assertTrue("Highly stable component" in Metrics.ia_analysis(0.1, 0.51))

    def test_ia_analysis_highly_unstable(self):
        self.assertTrue("Highly unstable component" in Metrics.ia_analysis(0.81, 0.49))

    def test_ia_analysis_low_abstract(self):
        self.assertTrue("Low abstract component" in Metrics.ia_analysis(0.51, 0.1))

    def test_ia_analysis_high_abstract(self):
        self.assertTrue("High abstract component" in Metrics.ia_analysis(0.49, 0.81))

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
        self.synthetic_data = SyntheticData.from_swift_file(swift_file=example_swiftfile)

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

    def test_add_data(self):
        additional_data = SyntheticData.from_swift_file(swift_file=example_swiftfile)
        self.synthetic_data += additional_data
        self.assertEqual(2, self.synthetic_data.loc)
        self.assertEqual(14, self.synthetic_data.noc)
        self.assertEqual(4, self.synthetic_data.number_of_concrete_data_structures)
        self.assertEqual(6, self.synthetic_data.number_of_interfaces)
        self.assertEqual(8, self.synthetic_data.number_of_methods)
        self.assertEqual(2, self.synthetic_data.number_of_tests)

    def test_subtract_data(self):
        additional_data = SyntheticData.from_swift_file(swift_file=example_swiftfile)
        self.synthetic_data -= additional_data
        self.assertEqual(0, self.synthetic_data.loc)
        self.assertEqual(0, self.synthetic_data.noc)
        self.assertEqual(0, self.synthetic_data.number_of_concrete_data_structures)
        self.assertEqual(0, self.synthetic_data.number_of_interfaces)
        self.assertEqual(0, self.synthetic_data.number_of_methods)
        self.assertEqual(0, self.synthetic_data.number_of_tests)

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
        self.framework_data = FrameworkData.from_swift_file(swift_file=example_swiftfile)

    def test_init_swift_file(self):
        self.assertEqual(1, self.framework_data.loc)
        self.assertEqual(7, self.framework_data.noc)
        self.assertEqual(2, self.framework_data.number_of_concrete_data_structures)
        self.assertEqual(3, self.framework_data.number_of_interfaces)
        self.assertEqual(4, self.framework_data.number_of_methods)
        self.assertEqual(1, self.framework_data.number_of_tests)
        self.assertEqual(2, self.framework_data.n_o_i)

    def test_append_framework(self):
        test_framework = Framework('Test')
        test_framework.append_import(Framework('Imported'))
        test_framework.submodule.files.append(example_swiftfile)

        self.framework_data.append_framework(test_framework)
        self.assertEqual(2, self.framework_data.loc)
        self.assertEqual(14, self.framework_data.noc)
        self.assertEqual(4, self.framework_data.number_of_concrete_data_structures)
        self.assertEqual(6, self.framework_data.number_of_interfaces)
        self.assertEqual(8, self.framework_data.number_of_methods)
        self.assertEqual(2, self.framework_data.number_of_tests)
        self.assertEqual(3, self.framework_data.n_o_i)

    def test_remove_framework_data(self):
        framework_additional_data = FrameworkData.from_swift_file(swift_file=example_swiftfile)

        self.framework_data -= framework_additional_data
        self.assertEqual(0, self.framework_data.loc)
        self.assertEqual(0, self.framework_data.noc)
        self.assertEqual(0, self.framework_data.number_of_concrete_data_structures)
        self.assertEqual(0, self.framework_data.number_of_interfaces)
        self.assertEqual(0, self.framework_data.number_of_methods)
        self.assertEqual(0, self.framework_data.number_of_tests)
        self.assertEqual(0, self.framework_data.n_o_i)

    def test_as_dict(self):
        expected_dict = {
            "loc": 1,
            "noc": 7,
            "n_a": 3,
            "n_c": 2,
            "nom": 4,
            "not": 1,
            "poc": 87.5,
            "noi": 2
        }
        self.assertEqual(expected_dict, self.framework_data.as_dict)


class SubModuleTests(unittest.TestCase):

    def setUp(self):
        self.submodule = SubModule(
            name="BusinessModule",
            files=[example_swiftfile],
            submodules=[],
            parent=None
        )
        self.helper = SubModule(
            name="Helper",
            files=[example_file2],
            submodules=[],
            parent=self.submodule
        )
        self.additional_module = SubModule(
            name="AdditionalModule",
            files=[example_file2],
            submodules=[],
            parent=self.submodule
        )
        self.additional_submodule = SubModule(
            name="AdditionalSubModule",
            files=[example_file2],
            submodules=[],
            parent=self.additional_module
        )
        self.additional_module.submodules.append(self.additional_submodule)
        self.submodule.submodules.append(self.helper)

    def test_n_of_files(self):
        self.assertEqual(2, self.submodule.n_of_files)

    def test_path(self):
        self.submodule.submodules.append(self.additional_module)
        self.assertEqual('BusinessModule > AdditionalModule > AdditionalSubModule', self.additional_submodule.path)

    def test_next_only_module(self):
        self.additional_submodule.parent = None
        self.assertEqual(self.additional_submodule, self.additional_submodule.next)

    def test_next_closed_circle(self):
        self.submodule.submodules.append(self.additional_module)
        #    *
        #   / \
        #  H   AM
        #       \
        #        AS
        self.assertEqual(self.helper, self.submodule.next)
        self.assertEqual(self.additional_module, self.helper.next)
        self.assertEqual(self.additional_submodule, self.additional_module.next)
        self.assertEqual(self.submodule, self.additional_submodule.next)

    def test_data(self):
        data = SyntheticData(
            loc=2,
            noc=14,
            number_of_interfaces=11,
            number_of_concrete_data_structures=6,
            number_of_methods=8,
            number_of_tests=2
        )
        self.assertEqual(data, self.submodule.data)

    def test_empty_data(self):
        data = SyntheticData(
            loc=0,
            noc=0,
            number_of_interfaces=0,
            number_of_concrete_data_structures=0,
            number_of_methods=0,
            number_of_tests=0
        )
        self.assertEqual(data, SubModule(name="", files=[], submodules=[], parent=None).data)

    def test_dict_repr(self):
        self.assertEqual({
            "BusinessModule": {
                "n_of_files": 2,
                "metric": {
                    "loc": 2,
                     "n_a": 11,
                     "n_c": 6,
                     "noc": 14,
                     "nom": 8,
                     "not": 2,
                     "poc": 87.5
                },
                "submodules": [
                    {
                        "Helper": {
                            "n_of_files": 1,
                            "metric": {
                                "loc": 1,
                                "n_a": 8,
                                "n_c": 4,
                                "noc": 7,
                                "nom": 4,
                                "not": 1,
                                "poc": 87.5
                            },
                            "submodules": []
                        }
                    }
                ]
            }
        }, self.submodule.as_dict)


if __name__ == '__main__':
    unittest.main()
