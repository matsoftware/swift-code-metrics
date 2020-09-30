from ._helpers import AnalyzerHelpers, Log, ParsingHelpers, ReportingHelpers
from ._parser import SwiftFile
from dataclasses import dataclass
from functional import seq
from typing import Dict, List, Optional


class Metrics:

    @staticmethod
    def distance_main_sequence(framework: 'Framework', frameworks: List['Framework']) -> float:
        """
        Distance from the main sequence (sweet spot in the A/I ratio)
        D³ = |A+I-1|
        D = 0: the component is on the Main Sequence (optimal)
        D = 1: the component is at the maximum distance from the main sequence (worst case)
        :param framework: The framework to analyze
        :param frameworks: The other frameworks in the project
        :return: the D³ value (from 0 to 1)
        """
        return abs(Metrics.abstractness(framework) + Metrics.instability(framework, frameworks) - 1)

    @staticmethod
    def instability(framework: 'Framework', frameworks: List['Framework']) -> float:
        """
        Instability: I = fan-out / (fan-in + fan-out)
        I = 0: maximally stable component
        I = 1: maximally unstable component
        :param framework: The framework to analyze
        :param frameworks: The other frameworks in the project
        :return: the instability value (float)
        """
        fan_in = Metrics.fan_in(framework, frameworks)
        fan_out = Metrics.fan_out(framework)
        sum_in_out = fan_in + fan_out
        if sum_in_out == 0:
            Log.warn(f'{framework.name} is not linked with the rest of the project.')
            return 0
        return fan_out / sum_in_out

    @staticmethod
    def abstractness(framework: 'Framework') -> float:
        """
        A = Na / Nc
        A = 0: maximally abstract component
        A = 1: maximally concrete component
        :param framework: The framework to analyze
        :return: The abstractness value (float)
        """
        if framework.data.number_of_concrete_data_structures == 0:
            Log.warn(f'{framework.name} is an external dependency.')
            return 0
        else:
            return framework.data.number_of_interfaces / framework.data.number_of_concrete_data_structures

    @staticmethod
    def fan_in(framework: 'Framework', frameworks: List['Framework']) -> int:
        """
        Fan-In: incoming dependencies (number of classes outside the framework that depend on classes inside it)
        :param framework: The framework to analyze
        :param frameworks: The other frameworks in the project
        :return: The Fan-In value (int)
        """
        fan_in = 0
        for f in Metrics.__other_nontest_frameworks(framework, frameworks):
            existing = f.imports.get(framework, 0)
            fan_in += existing
        return fan_in

    @staticmethod
    def fan_out(framework: 'Framework') -> int:
        """
        Fan-Out: outgoing dependencies. (number of classes inside this component that depend on classes outside it)
        :param framework: The framework to analyze
        :return: The Fan-Out value (int)
        """
        fan_out = 0
        for _, value in framework.imports.items():
            fan_out += value
        return fan_out

    @staticmethod
    def external_dependencies(framework: 'Framework', frameworks: List['Framework']) -> List['Dependency']:
        """
        :param framework: The framework to inspect for imports
        :param frameworks: The other frameworks in the project
        :return: List of imported frameworks that are external to the project (e.g third party libraries).
        System libraries excluded.
        """
        return Metrics.__filtered_imports(framework, frameworks, is_internal=False)

    @staticmethod
    def internal_dependencies(framework: 'Framework', frameworks: List['Framework']) -> List['Dependency']:
        """
        :param framework: The framework to inspect for imports
        :param frameworks: The other frameworks in the project
        :return: List of imported frameworks that are internal to the project
        """
        return Metrics.__filtered_imports(framework, frameworks, is_internal=True)

    @staticmethod
    def total_dependencies(framework: 'Framework') -> List[str]:
        """
        :param framework: The framework to inspect
        :return: The list of imported frameworks description
        """
        return seq(framework.imports.items()) \
            .map(lambda f: f'{f[0].name}({str(f[1])})') \
            .list()

    @staticmethod
    def percentage_of_comments(noc: int, loc: int) -> float:
        """
        Percentage Of Comments (POC) = 100 * NoC / ( NoC + LoC)
        :param noc: The number of lines of comments
        :param loc: the number of lines of code
        :return: The POC value (double)
        """
        noc_loc = noc + loc
        if noc_loc == 0:
            return 0
        return 100 * noc / noc_loc

    # Analysis

    @staticmethod
    def ia_analysis(instability: float, abstractness: float) -> str:
        """
        Verbose qualitative analysis of instability and abstractness.
        :param instability: The instability value of the framework
        :param abstractness: The abstractness value of the framework
        :return: Textual analysis.
        """
        if instability <= 0.5 and abstractness <= 0.5:
            return 'Zone of Pain. Highly stable and concrete component - rigid, hard to extend (not abstract). ' \
                   'This component should not be volatile (e.g. a stable foundation library such as Strings).'
        elif instability >= 0.5 and abstractness >= 0.5:
            return 'Zone of Uselessness. Maximally abstract with few or no dependents - potentially useless. ' \
                   'This component is high likely a leftover that should be removed.'

        # Standard components

        res = ''

        # I analysis
        if instability < 0.2:
            res += 'Highly stable component (hard to change, responsible and independent). '
        elif instability > 0.8:
            res += 'Highly unstable component (lack of dependents, easy to change, irresponsible) '

        # A analysis

        if abstractness < 0.2:
            res += 'Low abstract component, few interfaces. '
        elif abstractness > 0.8:
            res += 'High abstract component, few concrete data structures. '

        return res

    @staticmethod
    def poc_analysis(poc: float) -> str:
        if poc <= 20:
            return 'The code is under commented. '
        if poc >= 40:
            return 'The code is over commented. '

        return ''

    # Internal

    @staticmethod
    def __other_nontest_frameworks(framework: 'Framework', frameworks: List['Framework']) -> List['Framework']:
        return seq(frameworks) \
            .filter(lambda f: f is not framework and not f.is_test_framework) \
            .list()

    @staticmethod
    def __filtered_imports(framework: 'Framework',
                           frameworks: List['Framework'],
                           is_internal: bool) -> List['Dependency']:
        return seq(framework.imports.items()) \
            .filter(lambda f: (Metrics.__is_name_contained_in_list(f[0], frameworks)) == is_internal) \
            .map(lambda imp: Dependency(name=framework.name,
                                        dependent_framework=imp[0].name,
                                        number_of_imports=imp[1])) \
            .list()

    @staticmethod
    def __is_name_contained_in_list(framework: 'Framework', frameworks: List['Framework']) -> bool:
        return len(seq(frameworks)
                   .filter(lambda f: f.name == framework.name)
                   .list()) > 0


@dataclass
class SyntheticData:
    """
    Representation of synthetic code metric data
    """
    loc: int = 0
    noc: int = 0
    number_of_interfaces: int = 0
    number_of_concrete_data_structures: int = 0
    number_of_methods: int = 0
    number_of_tests: int = 0

    @classmethod
    def from_swift_file(cls, swift_file: Optional['SwiftFile'] = None) -> 'SyntheticData':
        return SyntheticData(
            loc=0 if swift_file is None else swift_file.loc,
            noc=0 if swift_file is None else swift_file.n_of_comments,
            number_of_interfaces=0 if swift_file is None else len(swift_file.interfaces),
            number_of_concrete_data_structures=0 if swift_file is None else \
                len(swift_file.structs + swift_file.classes),
            number_of_methods=0 if swift_file is None else len(swift_file.methods),
            number_of_tests=0 if swift_file is None else len(swift_file.tests)
        )

    def __add__(self, data):
        """
        Implementation of the `+` operator
        :param data: An instance of SyntheticData
        :return: a new instance of SyntheticData
        """
        return SyntheticData(
            loc=self.loc + data.loc,
            noc=self.noc + data.noc,
            number_of_interfaces=self.number_of_interfaces + data.number_of_interfaces,
            number_of_concrete_data_structures=self.number_of_concrete_data_structures
                                               + data.number_of_concrete_data_structures,
            number_of_methods=self.number_of_methods + data.number_of_methods,
            number_of_tests=self.number_of_tests + data.number_of_tests
        )

    def __sub__(self, data):
        """
        Implementation of the `-` operator
        :param data: An instance of SyntheticData
        :return: a new instance of SyntheticData
        """
        return SyntheticData(
            loc=self.loc - data.loc,
            noc=self.noc - data.noc,
            number_of_interfaces=self.number_of_interfaces - data.number_of_interfaces,
            number_of_concrete_data_structures=self.number_of_concrete_data_structures
                                               - data.number_of_concrete_data_structures,
            number_of_methods=self.number_of_methods - data.number_of_methods,
            number_of_tests=self.number_of_tests - data.number_of_tests
        )

    @property
    def poc(self) -> float:
        return Metrics.percentage_of_comments(self.noc, self.loc)

    @property
    def as_dict(self) -> Dict:
        return {
            "loc": self.loc,
            "noc": self.noc,
            "n_a": self.number_of_interfaces,
            "n_c": self.number_of_concrete_data_structures,
            "nom": self.number_of_methods,
            "not": self.number_of_tests,
            "poc": ReportingHelpers.decimal_format(self.poc)
        }


@dataclass()
class FrameworkData(SyntheticData):
    """
    Enriched synthetic data
    """
    n_o_i: int = 0

    @classmethod
    def from_swift_file(cls, swift_file: Optional['SwiftFile'] = None) -> 'FrameworkData':
        sd = SyntheticData.from_swift_file(swift_file=swift_file)
        return FrameworkData.__from_sd(sd=sd,
                                       n_o_i=0 if swift_file is None else \
                                           len([imp for imp in swift_file.imports if imp not in \
                                                AnalyzerHelpers.APPLE_FRAMEWORKS]))

    def __add__(self, data):
        """
        Implementation of the `+` operator
        :param data: An instance of FrameworkData
        :return: a new instance of FrameworkData
        """
        sd = self.__current_sd().__add__(data=data)
        return FrameworkData.__from_sd(sd=sd, n_o_i=self.n_o_i + data.n_o_i)

    def __sub__(self, data):
        """
        Implementation of the `-` operator
        :param data: An instance of FrameworkData
        :return: a new instance of FrameworkData
        """
        sd = self.__current_sd().__sub__(data=data)
        return FrameworkData.__from_sd(sd=sd, n_o_i=self.n_o_i - data.n_o_i)

    def append_framework(self, f: 'Framework'):
        sd = f.data
        self.loc += sd.loc
        self.noc += sd.noc
        self.number_of_interfaces += sd.number_of_interfaces
        self.number_of_concrete_data_structures += sd.number_of_concrete_data_structures
        self.number_of_methods += sd.number_of_methods
        self.number_of_tests += sd.number_of_tests
        self.n_o_i += f.number_of_imports

    @property
    def as_dict(self) -> Dict:
        return {**super().as_dict, **{"noi": self.n_o_i}}

    # Private

    def __current_sd(self) -> 'SyntheticData':
        return SyntheticData(
            loc=self.loc,
            noc=self.noc,
            number_of_interfaces=self.number_of_interfaces,
            number_of_concrete_data_structures=self.number_of_concrete_data_structures,
            number_of_methods=self.number_of_methods,
            number_of_tests=self.number_of_tests
        )

    @classmethod
    def __from_sd(cls, sd: 'SyntheticData', n_o_i: int) -> 'FrameworkData':
        return FrameworkData(
            loc=sd.loc,
            noc=sd.noc,
            number_of_interfaces=sd.number_of_interfaces,
            number_of_concrete_data_structures=sd.number_of_concrete_data_structures,
            number_of_methods=sd.number_of_methods,
            number_of_tests=sd.number_of_tests,
            n_o_i=n_o_i
        )


class Framework:
    def __init__(self, name: str, is_test_framework: bool = False):
        self.name = name
        self.__total_imports = {}
        self.submodule = SubModule(
            name=self.name,
            files=[],
            submodules=[],
            parent=None
        )
        self.is_test_framework = is_test_framework

    def __repr__(self):
        return self.name + '(' + str(self.number_of_files) + ' files)'

    def append_import(self, framework_import: 'Framework'):
        """
        Adds the dependent framework to the list of imported dependencies
        :param framework_import: The framework that is being imported
        :return:
        """
        existing_framework = self.__total_imports.get(framework_import)
        if not existing_framework:
            self.__total_imports[framework_import] = 1
        else:
            self.__total_imports[framework_import] += 1

    @property
    def data(self) -> SyntheticData:
        """
        The metrics data describing the framework
        :return: an instance of SyntheticData
        """
        return self.submodule.data

    @property
    def number_of_files(self) -> int:
        """
        Number of files in the framework
        :return: The total number of files in this framework (int)
        """
        return self.submodule.n_of_files

    @property
    def imports(self) -> Dict[str, int]:
        """
        Returns the list of framework imports without Apple libraries
        :return: list of filtered imports
        """
        return Framework.__filtered_imports(self.__total_imports.items())

    @property
    def number_of_imports(self) -> int:
        """
        :return: The total number of imports for this framework
        """
        return ParsingHelpers.reduce_dictionary(self.imports)

    @property
    def compact_name(self) -> str:
        all_capitals = ''.join(c for c in self.name if c.isupper())
        if len(all_capitals) > 4:
            return all_capitals[0] + all_capitals[-1:]
        elif len(all_capitals) == 0:
            return self.name[0]
        else:
            return all_capitals

    @property
    def compact_name_description(self) -> str:
        return f'{self.compact_name} = {self.name}'

    # Static

    @staticmethod
    def __filtered_imports(items: 'ItemsView') -> Dict[str, int]:
        return seq(items).filter(lambda f: f[0].name not in AnalyzerHelpers.APPLE_FRAMEWORKS).dict()


@dataclass
class SubModule:
    """
    Representation of a submodule inside a Framework
    """
    name: str
    files: List['SwiftFile']
    submodules: List['SubModule']
    parent: Optional['SubModule']

    @property
    def next(self) -> 'SubModule':
        if len(self.submodules) == 0:
            if self.parent is None:
                return self
        else:
            return self.submodules[0]

        next_level = self.parent
        current_level = self
        while next_level is not None:
            next_i = next_level.submodules.index(current_level) + 1
            if next_i < len(next_level.submodules):
                return next_level.submodules[next_i]
            else:
                current_level = next_level
                next_level = next_level.parent

        return current_level

    @property
    def n_of_files(self) -> int:
        sub_files = 0 if (len(self.submodules) == 0) else \
            seq([s.n_of_files for s in self.submodules]).reduce(lambda a, b: a + b)
        return len(self.files) + sub_files

    @property
    def path(self) -> str:
        parent_path = "" if not self.parent else f'{self.parent.path} > '
        return f'{parent_path}{self.name}'

    @property
    def data(self) -> 'SyntheticData':
        root_module_files = [SyntheticData()] if (len(self.files) == 0) else \
            [SyntheticData.from_swift_file(swift_file=f) for f in self.files]
        submodules_files = SyntheticData() if (len(self.submodules) == 0) else \
            seq([s.data for s in self.submodules]).reduce(lambda a, b: a + b)
        return seq(root_module_files).reduce(lambda a, b: a + b) + submodules_files

    @property
    def as_dict(self) -> Dict:
        return {
            self.name: {
                "n_of_files": self.n_of_files,
                "metric": self.data.as_dict,
                "submodules": [s.as_dict for s in self.submodules]
            }
        }


@dataclass
class Dependency:
    name: str
    dependent_framework: str
    number_of_imports: int = 0

    def __eq__(self, other):
        return (self.name == other.name) and \
               (self.dependent_framework == other.dependent_framework) and \
               (self.number_of_imports == other.number_of_imports)

    def __repr__(self):
        return f'{self.name} - {self.dependent_framework} ({str(self.number_of_imports)}) imports'

    @property
    def compact_repr(self) -> str:
        return f'{self.name} ({str(self.number_of_imports)})'

    @property
    def relationship(self) -> str:
        return f'{self.name} > {self.dependent_framework}'
