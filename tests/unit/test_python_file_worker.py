import builtins
import os

import pytest

from dp_builder.const import ROOT_PATH
from dp_builder.pythons_file_worker import PythonFileWorker

settings_path = os.path.join(ROOT_PATH, 'tests', 'unit', 'data', 'settings.py')
settings_content = """#Test sections to check get sections
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '%0@927=^*9s624(y55c@avd&ff*%11&v&fw=(xpx%5o7s@l18e'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
  'contrib.admin',
  'auth',
]

MIDDLEWARE = [
  'django.middleware',
  'django.contrib',
]

ROOT_URLCONF = 'my_project.urls'

TEMPLATES = [
  {
    'OPTIONS': {'cont_proc': ['cont_proc.messages',]
  },
]

DATABASES = {
  'default': {
    'ENGINE': 'sqlite3',
    'NAME': BD / 'sqlite3',
  }
}"""


@pytest.fixture
def settings_template() -> str:
    with open(settings_path, 'r') as file:
        settings = file.read()
    return settings


@pytest.fixture
def settings() -> str:
    return PythonFileWorker()


@pytest.fixture
def settings_with_sections():
    settings = PythonFileWorker()
    settings._content = settings_content
    return settings


@pytest.mark.parametrize(
    "section_name, is_collection, var_symbol, expected", [
        ("SECRET_KEY", False, "'", "SECRET_KEY = '%0@927=^*9s624(y55c@avd&ff*%11&v&fw=(xpx%5o7s@l18e'"),
        ("DATABASES", True, "{", "DATABASES = {\n  'default': {\n    'ENGINE': 'sqlite3',\n"
                           "    'NAME': BD / 'sqlite3',\n  }\n}"),
        ("INSTALLED_APPS", True, "[", "INSTALLED_APPS = [\n  'contrib.admin',\n  'auth',\n]"),
        ("ALLOWED_HOSTS", True, "[", "ALLOWED_HOSTS = []"),
        ("BASE_DIR", False, "P", "BASE_DIR = Path(__file__).resolve().parent.parent"),
        ("TEMPLATES", True, "[", "TEMPLATES = [\n  {\n    'OPTIONS': {'cont_proc': ['cont_proc.messages',]\n  },\n]"),
    ]
)
def test_get_section(settings_with_sections, section_name, var_symbol, is_collection, expected):
    result, start, end, is_collection, variable_pos = settings_with_sections.get_section(section_name)
    assert result == expected
    assert settings_with_sections._content[start: end+1] == expected
    assert settings_with_sections._content[variable_pos] == var_symbol


@pytest.mark.parametrize(
    'name, value, is_prepend, content, expected', [
        ('APPS', "'test'", False,
         "#Ext_test\nAPPS = [\n  'val_1',\n  'val_2',\n]\nOTHER = [\n]\n",
         "#Ext_test\nAPPS = [\n  'val_1',\n  'val_2',\n    'test',\n]\nOTHER = [\n]\n"),
        ('APPS', "'test'", True,
         "#Ext_test\nAPPS = [\n  'val_1',\n  'val_2',\n]\nOTHER = [\n]\n",
         "#Ext_test\nAPPS = [\n    'test',\n  'val_1',\n  'val_2',\n]\nOTHER = [\n]\n"),
    ]
)
def test_extend_section(settings, name, value, is_prepend, content, expected):
    settings._content = content
    settings.extend_section(name, value, prepend=is_prepend)
    assert settings._content == expected

@pytest.mark.parametrize(
    'variable, section, expected', [
        ("APPS", "APPS = [\n'val_1',\n'val_2',\n]", "#appl\nAPPS = [\n'val_1',\n'val_2',\n]\nVAR = var_1\nMID = []\n"),
        ("VAR", "VAR = 1024", "#appl\nAPPS = [\n'test_1',\n'test_2',\n]\nVAR = 1024\nMID = []\n"),
        ("MID", "TEST = 'Hello'", "#appl\nAPPS = [\n'test_1',\n'test_2',\n]\nVAR = var_1\nTEST = 'Hello'\n")
    ]
)
def test_replace_section(settings, variable, section, expected):
    settings._content = "#appl\nAPPS = [\n'test_1',\n'test_2',\n]\nVAR = var_1\nMID = []\n"
    settings.replace_section(settings.get_section(variable), section)
    assert settings._content == expected

@pytest.mark.parametrize(
    'variable, value, expected', [
        ("APPS", "Test", "#appl\nAPPS = Test\nVAR = var_1\nMID = []\n"),
        ("VAR", "1024", "#appl\nAPPS = [\n'test_1',\n'test_2',\n]\nVAR = 1024\nMID = []\n"),
    ]
)
def test_replace_section(settings, variable, value, expected):
    settings._content = "#appl\nAPPS = [\n'test_1',\n'test_2',\n]\nVAR = var_1\nMID = []\n"
    settings.replace_value(variable, value)
    assert settings._content == expected


def test_append_after(settings):
    settings._content = "#applications\nINSTALLED_APPS = [\n'test_1'\n]\nMIDDLEWARE = []"
    expected = "#applications\nINSTALLED_APPS = [\n'test_1'\n]\nTEST = []\nMIDDLEWARE = []"
    settings.append_after('INSTALLED_APPS', 'TEST = []')
    assert settings._content == expected


@pytest.mark.parametrize(
    'from_val, import_val, expected_str',
    [
        (None, 'test', 'import test\n'),
        ('xyz', 'abc', 'from xyz import abc\n'),
        ('xy', 'yx', ''),
    ]
)
def test_add_import(from_val, import_val, expected_str, settings):
    settings._content = 'import abc\nfrom xy import yx\nurlpatterns = []'
    expected = f'import abc\nfrom xy import yx\n{expected_str}urlpatterns = []'
    settings.add_import(import_val, from_val)
    assert settings._content == expected


def test_load_settings(settings_template, settings):
    settings.load(settings_path)
    assert settings._content == settings_template


def test_write_settings(settings, mocker):
    mocker.patch('builtins.open', autospec=True)

    settings._content = 'test_data'
    settings.save('here')

    builtins.open.assert_called_once_with('here', 'w')
    handle = builtins.open.return_value.__enter__.return_value
    handle.write.assert_called_once_with('test_data')


