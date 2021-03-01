import re
from typing import Dict, Any

from dp_builder.pythons_file_worker import PythonFileWorker


class Environments:
    def __init__(self, settings: PythonFileWorker):
        self._data: Dict[str, Any] = {}
        self.settings = settings

    def _create_settings_value(self, val_type: type, name: str, default: any) -> str:
        if default is not None and val_type != type(default):
            raise ValueError(f"The types for value of setting {name}, and default value must be same")
        if val_type is str:
            return f"os.environ.get('{name}', {default})"
        if val_type is int:
            return f"int(os.environ.get('{name}', {default}))"
        if val_type is list:
            if default is not None:
                default = " ".join(default)
                default = f"'{default}'"
            return f"os.environ.get('{name}', {default}).split(' ')"

    def set(self, env_name: str, value: Any):
        self._data[env_name] = value

    def bind_to_setting(self, settings_name: str, env_name: str = None, value: Any = '', default: Any = None):
        if env_name is None:
            env_name = f'{settings_name}_ENV'
        settings_value = self._create_settings_value(type(value), env_name, default)
        self.settings.replace_value(settings_name, settings_value)
        self._data[env_name] = value

    def save(self, path):
        with open(path, 'w') as file:
            file.write(self.get_result())

    def get_val_from_line(self, line):
        reg = r"([A-Z0-9_]+) *= *(.+)"
        match = re.match(reg, line)
        if match is not None:
            return {match[1]: match[2]}
        return None

    def load(self, path):
        result = {}
        with open(path, 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line_data = self.get_val_from_line(line)
                if line_data is not None:
                    result = {**result, **line_data}
        self._data = result

    def get_result(self):
        result = []
        for name, value in self._data.items():
            if type(value) is list:
                value = ' '.join([str(val) for val in value])
            result.append(f"{name}={value}\n")
        return ''.join(result)

    def __repr__(self):
        return self.get_result()
