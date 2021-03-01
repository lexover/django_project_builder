import re
from collections import namedtuple
from typing import List, NamedTuple


class Requirements:
    Package = namedtuple('Package', ['name', 'version'])

    def __init__(self):
        self._data: List[NamedTuple] = []

    def validate_version(self, version: str) -> bool:
        if version is None:
            return False
        return bool(re.match(r'\d{1,2}\.\d{1,2}\.\d{1,2}', version))

    def is_name_unique(self, name: str) -> bool:
        if name in [row.name for row in self._data]:
            return True

    def add(self, name: str, version: str = None):
        if self.is_name_unique(name):
            raise ValueError(f'Package with name `{name}` already in requirements')
        if version is not None:
            if not self.validate_version(version):
                raise ValueError(f'Specified package `{name}=={version}` version incorrect')
        self._data.append(self.Package(name, version))

    def get_result(self):
        result = []
        for val in self._data:
            if val.version is None:
               result.append(f'{val.name}\n')
            else:
                result.append(f'{val.name}=={val.version}\n')
        return ''.join(result)

    def save(self, path):
        with open(path, 'w') as file:
            file.write(self.get_result())

    def __repr__(self):
        return self.get_result()


