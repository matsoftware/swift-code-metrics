import os


class SwiftFile:
    def __init__(self, framework_name, imports, interfaces, concretes, methods):
        self.framework_name = framework_name
        self.imports = imports
        self.interfaces = interfaces
        self.concretes = concretes
        self.methods = methods


class SwiftFileParser:
    def __init__(self, file, base_path):
        self.file = file
        self.base_path = base_path
        self.imports = []
        self.attributes_modifiers = [
            'private',
            'fileprivate',
            'internal',
            'public',
            'final',
            'open'
        ]

    def parse(self):
        return SwiftFile(
            framework_name=self.__framework_name(),
            imports=self.__read_imports(),
            interfaces=self.__read_protocols(),
            concretes=self.__read_concrete_data_structures(),
            methods=self.__read_methods()
        )

    # Properties mapper

    def __framework_name(self):
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath(subdir)
        if first_subpath.endswith('.swift'):
            return 'AppTarget'
        else:
            return first_subpath

    def __read_imports(self):
        return self.__read_attribute('import')

    def __read_protocols(self):
        return self.__read_attribute('protocol', self.attributes_modifiers)

    def __read_concrete_data_structures(self):
        return self.__read_attribute('struct', self.attributes_modifiers) + \
               self.__read_attribute('class', self.attributes_modifiers)

    def __read_methods(self):
        return self.__read_attribute('func', ['', 'static'])

    # Private helpers

    def __extract_first_subpath(self, subdir):
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath(subdirs[0])
        else:
            return subdir.replace('/', '')

    def __read_attribute(self, attr_name, prefixed_attributes=None):
        """
        Extracts the attribute with a name from a line of the file, if exists
        @param attr_name: The attribute inspected (e.g. `class`, `protocol`)
        @param prefixed_attributes: The list of prefixed attributes to ignore
        @return: list of attributes matching the given pattern in the file
        """
        if prefixed_attributes is None:
            prefixed_attributes = []
        attrs = []
        with open(self.file) as f:
            for line in f:
                trimmed = line.strip()
                for a in prefixed_attributes:
                    trimmed = trimmed.replace(a, '')
                if trimmed.strip().startswith(attr_name):
                    attr = trimmed.replace(attr_name, '').strip()
                    attrs.append(attr)
        return attrs
