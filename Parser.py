import os

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
            'final'
        ]

    def framework_name(self):
        # filename: framework_name = os.path.basename(self.file)
        subdir = self.file.replace(self.base_path, '')
        first_subpath = self.__extract_first_subpath__(subdir)
        if first_subpath.endswith(".swift"):
            return "AppTarget"
        else:
            return first_subpath

    def read_imports(self):
        return self.__read_prefixed_attribute__('import')

    def read_protocols(self):
        return self.__read_prefixed_attribute__('protocol', self.attributes_modifiers)

    def read_concrete_data_structures(self):
        return self.__read_prefixed_attribute__('struct', self.attributes_modifiers) +\
               self.__read_prefixed_attribute__('class', self.attributes_modifiers)

        # Private

    def __extract_first_subpath__(self, subdir):
        subdirs = os.path.split(subdir)
        if len(subdirs[0]) > 1:
            return self.__extract_first_subpath__(subdirs[0])
        else:
            return subdir.replace('/', '')

    def __read_prefixed_attribute__(self, attr_name, attributes=[]):
        attrs = []
        with open(self.file) as f:
            for line in f:
                trimmed = line.strip()
                for a in attributes:
                    trimmed = trimmed.replace(a, '')
                if trimmed.strip().startswith(attr_name):
                    attr = trimmed.replace(attr_name, '').strip()
                    attrs.append(attr)
        return attrs
