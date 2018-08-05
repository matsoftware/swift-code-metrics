import os
import parser


class Inspector:
    def __init__(self, directory, exclude_paths=None):
        if exclude_paths is None:
            exclude_paths = []
        self.frameworks = []
        if directory is not None:
            self.__analyze_directory(directory, exclude_paths)

    # Analysis

    def global_frameworks_data(self):
        """
        It returns the global aggregated data for LOC, NOC, NA, NC and NBM using the analyzed frameworks.
        :return: A string containing the aggregate data synthesis.
        """
        loc = 0
        noc = 0
        n_a = 0
        n_c = 0
        nbm = 0
        for f in self.frameworks:
            loc += f.loc
            noc += f.noc
            n_a += f.number_of_interfaces
            n_c += f.number_of_concrete_data_structures
            nbm += f.number_of_methods

        poc = self.percentage_of_comments(noc, loc)
        poc_analysis = self.poc_analysis(poc)

        return f'''
Aggregate data:
LOC = {loc}
NOC = {noc}
POC = {"%.0f" % poc}% {poc_analysis}
Na = {n_a}
Nc = {n_c}
NBM = {nbm}
'''

    def framework_analysis(self, framework):
        """
        :param framework: The framework to analyze
        :return: The architectural analysis of the framework
        """
        loc = framework.loc
        noc = framework.noc
        poc = self.percentage_of_comments(framework.noc, framework.loc)
        poc_analysis = self.poc_analysis(poc)
        fan_in = self.fan_in(framework)
        fan_out = self.fan_out(framework)
        i = self.instability(framework)
        n_a = framework.number_of_interfaces
        n_c = framework.number_of_concrete_data_structures
        a = self.abstractness(framework)
        d_3 = self.distance_main_sequence(framework)
        nbm = framework.number_of_methods
        ia_analysis = self.ia_analysis(i, a)
        return f'''
Architectural analysis for {framework.name} ({framework.compact_name()}): \n
LOC = {loc}
NOC = {noc}
POC = {"%.0f" % poc}% {poc_analysis}
Fan In = {fan_in}
Fan Out = {fan_out}
Instability = {i}\n
Na = {n_a}
Nc = {n_c}
A = {a}\n
D3 = {d_3}\n
NBM = {nbm}\n
{ia_analysis}\n'''

    def ia_analysis(self, instability, abstractness):
        """
        Verbose qualitative analysis of instability and abstractness.
        :param instability: The instability value of the framework
        :param abstractness: The abstractness value of the framework
        :return: Textual analysis.
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

    def poc_analysis(self, poc):
        if poc <= 20:
            return '(under commented)'
        if poc >= 40:
            return '(over commented)'

        return ''

    # Metrics

    def distance_main_sequence(self, framework):
        """
        Distance from the main sequence (sweet spot in the A/I ratio)
        D³ = |A+I-1|
        D = 0: the component is on the Main Sequence (optimal)
        D = 1: the component is at the maximum distance from the main sequence (worst case)
        :param framework:
        :return:
        """
        return abs(self.abstractness(framework) + self.instability(framework) - 1)

    def instability(self, framework):
        """
        Instability: I = fan-out / (fan-in + fan-out)
        I = 0: maximally stable component
        I = 1: maximally unstable component
        :param framework: The framework to analyze
        :return: the instability value (double)
        """
        fan_in = self.fan_in(framework)
        fan_out = self.fan_out(framework)
        return fan_out / (fan_in + fan_out)

    def abstractness(self, framework):
        """
        A = Na / Nc
        A = 0: maximally abstract component
        A = 1: maximally concrete component
        :param framework: The framework to analyze
        :return: The abstractness value (double)
        """
        if framework.number_of_concrete_data_structures == 0:
            #  This is an external dependency build as source
            return 0
        else:
            return framework.number_of_interfaces / framework.number_of_concrete_data_structures

    def fan_in(self, framework):
        """
        Fan-In: incoming dependencies (number of classes outside the framework that depend on classes inside it)
        :param framework: The framework to analyze
        :return: The Fan-In value (int)
        """
        fan_in = 0
        for f in self.__other_frameworks(framework):
            existing = f.imports.get(framework, 0)
            fan_in += existing
        return fan_in

    def fan_out(self, framework):
        """
        Fan-Out: outgoing dependencies. (number of classes inside this component that depend on classes outside it)
        :param framework: The framework to analyze
        :return: The Fan-Out value (int)
        """
        fan_out = 0
        for key, value in framework.imports.items():
            fan_out += value
        return fan_out

    def percentage_of_comments(self, noc, loc):
        """
        Percentage Of Comments (POC) = 100 * NoC / ( NoC + LoC)
        :param noc: The number of lines of comments
        :param loc: the number of lines of code
        :return: The POC value (double)
        """
        return 100 * noc / (noc + loc)

    def coupled_frameworks(self, framework):
        """
        :param framework: The framework to inspect for coupled dependencies
        :return: List of dependent frameworks
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
                    swift_file = parser.SwiftFileParser(full_path, directory).parse()
                    self.__append_dependency(swift_file)
        self.__cleanup_external_dependencies()

    def __is_excluded_folder(self, subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False

    def __append_dependency(self, swift_file):
        framework = self.__get_or_create_framework(swift_file.framework_name)
        framework.number_of_files += 1
        framework.loc += swift_file.loc
        framework.noc += swift_file.n_of_comments
        framework.number_of_interfaces += len(swift_file.interfaces)
        framework.number_of_concrete_data_structures += len(swift_file.structs + swift_file.classes)
        framework.number_of_methods += len(swift_file.methods)

        for f in swift_file.imports:
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
        self.loc = 0
        self.noc = 0
        self.number_of_files = 0
        self.number_of_concrete_data_structures = 0
        self.number_of_interfaces = 0
        self.number_of_methods = 0
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
        all_capitals = ''.join(c for c in self.name if c.isupper())
        if len(all_capitals) > 2:
            return all_capitals[0] + all_capitals[-1:]
        elif len(all_capitals) == 0:
            return self.name[0]
        else:
            return all_capitals

    def compact_name_description(self):
        return self.compact_name() + ' = ' + self.name