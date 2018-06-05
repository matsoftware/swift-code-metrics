import os
import parser


class Inspector:
    def __init__(self, directory, exclude_paths=None):
        if exclude_paths is None:
            exclude_paths = []
        self.frameworks = []
        if not directory is None:
            self.__analyze_directory(directory, exclude_paths)

    # Metrics

    def instability_data(self):
        """
        @return: A tuple to represent the instability of each framework
        """
        sorted_instability = sorted(list(map(lambda f: (self.instability(f),
                                                        f.compact_name(),
                                                        f.compact_name_description()), self.frameworks)),
                                    key=lambda tup: tup[0])
        return (list(map(lambda f: f[0], sorted_instability)),
                list(map(lambda f: f[1], sorted_instability)),
                list(map(lambda f: f[2], sorted_instability)))

    def instability_abstractness_data(self):
        """
        @return: A tuple to represent instability and abstractness data on a scattered plot
        """
        return (list(map(lambda f: self.instability(f), self.frameworks)),
                list(map(lambda f: self.abstractness(f), self.frameworks)),
                list(map(lambda f: f.name, self.frameworks)))

    def framework_analysis(self, framework):
        """ 
        @param framework: The framework to analyze
        @return: The architectural analysis of the framework
        """
        fan_in = self.fan_in(framework)
        fan_out = self.fan_out(framework)
        i = self.instability(framework)
        n_a = framework.number_of_interfaces
        n_c = framework.number_of_concrete_data_structures
        a = self.abstractness(framework)
        d_3 = self.distance_main_sequence(framework)
        ia_analysis = self.ia_analysis(i, a)
        return f'''
Architectural analysis for {framework.name}: \n
Fan In = {fan_in}
Fan Out = {fan_out}
Instability = {i}\n
Na = {n_a}
Nc = {n_c}
A = {a}\n
D3 = {d_3}\n
{ia_analysis}\n'''

    def ia_analysis(self, instability, abstractness):
        """
        Verbose qualitative analysis of instability and abstractness.
        @param instability: The instability value of the framework
        @param abstractness: The abstractness value of the framework
        @return: Textual analysis.
        """
        if instability <= 0.5 and abstractness <= 0.5:
            return '(Zone of Pain). Highly stable and concrete component - rigid, hard to extend (not abstract).\n' \
                   'This component should not be volatile (e.g. a stable foundation library such as Strings).'
        elif instability >= 0.5 and abstractness >= 0.5:
            return '(Zone of Uselessness). Maximally abstract with few or no dependents - potentially useless.\n' \
                   'This component is high likely a leftover that should be removed.'

        # Standard components

        res = ''

        # I analysis
        if instability < 0.2:
            res += 'Highly stable component (hard to change, responsible and independent).\n'
        elif instability > 0.8:
            res += 'Highly unstable component (lack of dependents, easy to change, irresponsible)\n'

        # A analysis

        if abstractness < 0.2:
            res += 'Low abstract component, few interfaces.\n'
        elif abstractness > 0.8:
            res += 'High abstract component, few concrete data structures.\n'

        return res

    def distance_main_sequence(self, framework):
        """
        Distance from the main sequence (sweet spot in the A/I ratio)
        D³ = |A+I-1|
        D = 0: the component is on the Main Sequence (optimal)
        D = 1: the component is at the maximum distance from the main sequence (worst case)
        @param framework:
        @return:
        """
        return abs(self.abstractness(framework) + self.instability(framework) - 1)

    def instability(self, framework):
        """
        Instability: I = fan-out / (fan-in + fan-out)
        I = 0: maximally stable component
        I = 1: maximally unstable component
        @param framework: The framework to analyze
        @return: the instability value (double)
        """
        fan_in = self.fan_in(framework)
        fan_out = self.fan_out(framework)
        return fan_out / (fan_in + fan_out)

    def abstractness(self, framework):
        """
        A = Na / Nc
        A = 0: maximally abstract component
        A = 1: maximally concrete component
        @param framework: The framework to analyze
        @return: The abstractness value (double)
        """
        if framework.number_of_concrete_data_structures == 0:
            #  This is an external dependency build as source
            return 0
        else:
            return framework.number_of_interfaces / framework.number_of_concrete_data_structures

    def fan_in(self, framework):
        """
        Fan-In: incoming dependencies (number of classes outside the framework that depend on classes inside it)
        @param framework: The framework to analyze
        @return: The Fan-In value (int)
        """
        fan_in = 0
        for f in self.__other_frameworks(framework):
            existing = f.imports.get(framework, 0)
            fan_in += existing
        return fan_in

    def fan_out(self, framework):
        """
        Fan-Out: outgoing dependencies. (number of classes inside this component that depend on classes outside it)
        @param framework: The framework to analyze
        @return: The Fan-Out value (int)
        """
        fan_out = 0
        for key, value in framework.imports.items():
            fan_out += value
        return fan_out

    def coupled_frameworks(self, framework):
        """
        @param framework: The framework to inspect for coupled dependencies
        @return: List of dependent frameworks
        """
        couples = []
        for f in self.frameworks:
            if f.imports.get(framework):
                couples.append((framework.name, f.name))
        return couples

    # Directory inspection

    def __analyze_directory(self, directory, exclude_paths):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.swift') and \
                        not 'Test' in file \
                        and not self.__is_excluded_folder(subdir, exclude_paths):
                    full_path = os.path.join(subdir, file)
                    tr = parser.SwiftFile(full_path, directory)
                    framework_name = tr.framework_name()
                    imports = tr.read_imports()
                    interfaces = tr.read_protocols()
                    concretes = tr.read_concrete_data_structures()
                    self.__append_dependency(framework_name, imports, interfaces, concretes)
        self.__cleanup_external_dependencies()

    def __is_excluded_folder(self, subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False

    def __append_dependency(self, framework_name, imports, interfaces, concretes):
        framework = self.__get_or_create_framework(framework_name)
        framework.number_of_files += 1
        framework.number_of_interfaces += len(interfaces)
        framework.number_of_concrete_data_structures += len(concretes)

        for f in imports:
            imported_framework = self.__get_or_create_framework(f)
            if imported_framework is None:
                imported_framework = Framework(f)
            framework.append_import(imported_framework)

    def __cleanup_external_dependencies(self):
        # It will remove external dependencies built as source
        self.frameworks = list(filter(lambda f: f.number_of_files > 0, self.frameworks))

    def __get_or_create_framework(self, framework_name):
        framework = self.__get_framework(framework_name)
        if framework is None:
            # not found, create a new one
            framework = Framework(framework_name)
            self.frameworks.append(framework)
        return framework

    def __get_framework(self, name):
        for f in self.frameworks:
            if f.name == name:
                return f
        return None

    def __other_frameworks(self, framework):
        return list(filter(lambda f: f is not framework, self.frameworks))

    def __take_first(elem):
        return elem[0]

class Framework:
    def __init__(self, name):
        self.name = name
        self.number_of_files = 0
        self.number_of_concrete_data_structures = 0
        self.number_of_interfaces = 0
        self.imports = {}

    def __repr__(self):
        return self.name + '(' + str(self.number_of_files) + ' files)'

    def append_import(self, framework_import):
        existing_framework = self.imports.get(framework_import)
        if not existing_framework:
            self.imports[framework_import] = 1
        else:
            self.imports[framework_import] += 1

    def compact_name(self):
        return ''.join(c for c in self.name if c.isupper())

    def compact_name_description(self):
        return self.compact_name() + ' = ' + self.name
