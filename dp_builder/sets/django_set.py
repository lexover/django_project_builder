from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.sets import AbstractSet


class DjangoSet(AbstractSet):
    def __init__(self, settings, app_name):
        self.settings: PythonFileWorker = settings
        self.app_name: str = app_name

    def set(self):
        self.settings.extend_section('INSTALLED_APPS', f"'{self.app_name}'")
