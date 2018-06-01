
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

