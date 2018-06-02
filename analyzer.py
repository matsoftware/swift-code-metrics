import os
import parser


class Container:
    def __init__(self, directory, exclude_paths=None):
        if exclude_paths is None:
            exclude_paths = []
        self.frameworks = []
        self.__analyze_directory(directory, exclude_paths)

    # Metrics

    def instability_abstractness_data(self):
        return (list(map(lambda f: self.instability(f), self.frameworks)),
                list(map(lambda f: self.abstractness(f), self.frameworks)),
                list(map(lambda f: f.name, self.frameworks)))

    def framework_analysis(self, f):
        fan_in = self.fan_in(f)
        fan_out = self.fan_out(f)
        I = self.instability(f)
        Na = f.number_of_interfaces
        Nc = f.number_of_concrete_data_structures
        A = self.abstractness(f)
        D3 = self.distance_main_sequence(f)
        ia_analysis = self.ia_analysis(I, A)
        return f'''
Architectural analysis for {f.name}: \n
Fan In = {fan_in}
Fan Out = {fan_out}
Instability = {I}\n
Na = {Na}
Nc = {Nc}
A = {A}\n
D3 = {D3}\n
{ia_analysis}\n'''

    def ia_analysis(self, I, A):
        if I <= 0.5 and A <= 0.5:
            return "(Zone of Pain). Highly stable and concrete component - rigid, hard to extend (not abstract).\n" \
                   "This component should not be volatile (e.g. a stable foundation library such as Strings)."
        elif I >= 0.5 and A >= 0.5:
            return "(Zone of Uselessness). Maximally abstract with few or no dependents - potentially useless.\n" \
                   "This component is high likely a leftover that should be removed."

        # Standard components

        res = ""

        # I analysis
        if I < 0.2:
            res += "Highly stable component (hard to change, responsible and independent).\n"
        elif I > 0.8:
            res += "Highly unstable component (lack of dependents, easy to change, irresponsible)\n"

        # A analysis

        if A < 0.2:
            res += "Low abstract component, few interfaces.\n"
        elif A > 0.8:
            res += "High abstract component, few concrete data structures.\n"

        return res

    def distance_main_sequence(self, framework):
        return abs(self.abstractness(framework) + self.instability(framework) - 1)

    def instability(self, framework):
        # Instability: I = fan-out / (fan-in + fan-out)
        # I = 0: maximally stable component
        # I = 1: maximally unstable component
        fan_in = self.fan_in(framework)
        fan_out = self.fan_out(framework)
        return fan_out / (fan_in + fan_out)

    def abstractness(self, framework):
        # A = Na / Nc
        if framework.number_of_concrete_data_structures == 0:
            #  This is an external dependency build as source
            return 0
        else:
            return framework.number_of_interfaces / framework.number_of_concrete_data_structures

    def fan_in(self, framework):
        # Fan-In: incoming dependencies (number of classes outside the framework that depend on classes inside it)
        fan_in = 0
        for f in self.__other_frameworks(framework):
            existing = f.imports.get(framework, 0)
            fan_in += existing
        return fan_in

    def fan_out(self, framework):
        # Fan-Out: outgoing dependencies. (number of classes inside this component
        # that depend on classes outside the component)
        fan_out = 0
        for key, value in framework.imports.items():
            fan_out += value
        return fan_out

    def coupled_frameworks(self, framework):
        couples = []
        for f in self.frameworks:
            if f.imports.get(framework):
                couples.append((framework.name, f.name))
        return couples

    # Directory inspection

    def __analyze_directory(self, directory, exclude_paths):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".swift") and \
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
