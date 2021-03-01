import re
from typing import Dict

class TemplateHandler:
    def __init__(self, path: str):
        self._path = self._path
        self._content = self._load_data(path)

    def _load_data(self, path: str):
        with open(path, 'r') as file:
            return file.read()

    def set(self, data: Dict[str, str]) -> None:
        for key, val in data:
            self._content = self._content.replace(''.join(["{{", key, "}}"]), val)

    def is_complete(self) -> bool:
        reg = "\{\{ *.+ *\}\}"
        return True if re.search(reg, self._content, flags=re.MULTILINE) is None else False

    def save(self) -> None:
        with open(self._path, 'w') as file:
            file.save(self._content)