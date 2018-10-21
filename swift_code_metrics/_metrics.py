

class Metrics:

    @staticmethod
    def distance_main_sequence(framework, frameworks):
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
    def instability(framework, frameworks):
        """
        Instability: I = fan-out / (fan-in + fan-out)
        I = 0: maximally stable component
        I = 1: maximally unstable component
        :param framework: The framework to analyze
        :param frameworks: The other frameworks in the project
        :return: the instability value (double)
        """
        fan_in = Metrics.fan_in(framework, frameworks)
        fan_out = Metrics.fan_out(framework)
        return fan_out / (fan_in + fan_out)

    @staticmethod
    def abstractness(framework):
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

    @staticmethod
    def fan_in(framework, frameworks):
        """
        Fan-In: incoming dependencies (number of classes outside the framework that depend on classes inside it)
        :param framework: The framework to analyze
        :param frameworks: The other frameworks in the project
        :return: The Fan-In value (int)
        """
        fan_in = 0
        for f in Metrics.__other_frameworks(framework, frameworks):
            existing = f.imports.get(framework, 0)
            fan_in += existing
        return fan_in

    @staticmethod
    def fan_out(framework):
        """
        Fan-Out: outgoing dependencies. (number of classes inside this component that depend on classes outside it)
        :param framework: The framework to analyze
        :return: The Fan-Out value (int)
        """
        fan_out = 0
        for key, value in framework.imports.items():
            fan_out += value
        return fan_out

    @staticmethod
    def external_dependencies(framework, frameworks):
        """
        :param framework: The framework to inspect for imports
        :param frameworks: The other frameworks in the project
        :return: List of imported frameworks that are external to the project (e.g. system or third party libraries)
        """
        return Metrics.__filtered_imports(framework, frameworks, is_internal=False)

    @staticmethod
    def internal_dependencies(framework, frameworks):
        """
        :param framework: The framework to inspect for imports
        :param frameworks: The other frameworks in the project
        :return: List of imported frameworks that are internal to the project
        """
        return Metrics.__filtered_imports(framework, frameworks, is_internal=True)

    @staticmethod
    def percentage_of_comments(noc, loc):
        """
        Percentage Of Comments (POC) = 100 * NoC / ( NoC + LoC)
        :param noc: The number of lines of comments
        :param loc: the number of lines of code
        :return: The POC value (double)
        """
        return 100 * noc / (noc + loc)

    # Analysis

    @staticmethod
    def ia_analysis(instability, abstractness):
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
    def poc_analysis(poc):
        if poc <= 20:
            return 'The code is under commented. '
        if poc >= 40:
            return 'The code is over commented. '

        return ''

    # Internal

    @staticmethod
    def __other_frameworks(framework, frameworks):
        return list(filter(lambda f: f is not framework, frameworks))

    @staticmethod
    def __filtered_imports(framework, frameworks, is_internal):
        return list(
            map(lambda imp: Dependency(imp[0].name, imp[1]),
                dict(filter(lambda f: (Metrics.__is_name_contained_in_list(f[0], frameworks)) == is_internal,
                            framework.imports.items())).items()
            )
        )

    @staticmethod
    def __is_name_contained_in_list(framework, frameworks):
        return len(list(
            filter(lambda f: f.name == framework.name, frameworks)
        )) > 0


class Framework:
    def __init__(self, name):
        self.name = name
        self.loc = 0
        self.noc = 0
        self.number_of_files = 0
        self.number_of_concrete_data_structures = 0
        self.number_of_interfaces = 0
        self.number_of_methods = 0
        self.number_of_tests = 0
        self.imports = {}
        self.is_test_framework = False

    def __repr__(self):
        return self.name + '(' + str(self.number_of_files) + ' files)'

    def append_import(self, framework_import):
        existing_framework = self.imports.get(framework_import)
        if not existing_framework:
            self.imports[framework_import] = 1
        else:
            self.imports[framework_import] += 1

    @property
    def compact_name(self):
        all_capitals = ''.join(c for c in self.name if c.isupper())
        if len(all_capitals) > 3:
            return all_capitals[0] + all_capitals[-1:]
        elif len(all_capitals) > 1:
            return all_capitals
        elif len(all_capitals) == 0:
            return self.name[0]
        else:
            return all_capitals

    @property
    def compact_name_description(self):
        return self.compact_name + ' = ' + self.name


class Dependency:
    def __init__(self, framework, number_of_imports=0):
        self.framework = framework
        self.number_of_imports = number_of_imports

    def __eq__(self, other):
        return (self.framework == other.framework) and \
               (self.number_of_imports == other.number_of_imports)

    def __repr__(self):
        return self.framework + '(' + str(self.number_of_imports) + ' imports)'
