from unittest.mock import mock_open

import pytest

from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.environments import Environments


@pytest.fixture
def settings() -> PythonFileWorker:
    settings = PythonFileWorker()
    settings._content = """
TEST_1 = value_1
TEST_2 = value_2

SOME_DICT = {
   'TEST_DICT': 'Dict_val',
}
   TEST_3 = value_3
"""
    return settings


@pytest.fixture
def env_variables():
    return {
        'TEST_1': 'test_1',
        'TEST_2': "'test_2'",
        'TEST_3': '1024',
    }


@pytest.mark.parametrize(
    'setting_name, env_name, value, default, exp_setting', [
        ('TEST_1', None, '', None, "TEST_1 = os.environ.get('TEST_1_ENV', None)"),
        ('TEST_1', None, '', None, "TEST_1 = os.environ.get('TEST_1_ENV', None)"),
        ('TEST_2', 'MY_TEST', 'val', None, "TEST_2 = os.environ.get('MY_TEST', None)"),
        ('TEST_3', None, 10, None, "TEST_3 = int(os.environ.get('TEST_3_ENV', None))"),
        ('TEST_3', None, ['a', 'b'], None, "TEST_3 = os.environ.get('TEST_3_ENV', None).split(' ')"),
        ('TEST_3', None, ['a', 'b'], ['a', 'b'], "TEST_3 = os.environ.get('TEST_3_ENV', 'a b').split(' ')"),
    ]
)
def test_variables_to_setting(settings, env_variables, setting_name, env_name, value, default, exp_setting):
    env = Environments(settings)
    env.bind_to_setting(settings_name=setting_name, env_name=env_name, value=value, default=default)
    env_name = f'{setting_name}_ENV' if env_name is None else env_name
    assert env._data.get(env_name) == value
    assert settings.get_section(setting_name).content == exp_setting


@pytest.mark.parametrize(
    "data, expected", [
        ({"TEST_1": "Value"}, "TEST_1=Value\n"),
        ({"TEST_1": "Val_1", "TEST_2": "Val_2"}, "TEST_1=Val_1\nTEST_2=Val_2\n"),
        ({"TEST_1": 1, "TEST_2": 2}, "TEST_1=1\nTEST_2=2\n"),
        ({"TEST_1": [1, 2, 3], "TEST_2": "Val_2"}, "TEST_1=1 2 3\nTEST_2=Val_2\n"),
        ({"TEST_1": ['ab', 'bc', 'xy'], "TEST_2": "Val_2"}, "TEST_1=ab bc xy\nTEST_2=Val_2\n"),
    ]
)
def test_get_result(data, expected):
    env = Environments(None)
    env._data = data
    assert env.get_result() == expected

def test_get_value_from_line():
    env = Environments(None)
    assert env.get_val_from_line("TEST_1 = val_1") == {"TEST_1": "val_1"}


def test_load(mocker):
    mocker.patch('builtins.open', mock_open(read_data="TEST_1 = val_1\nTEST_2 = val_2\n\nTEST_3 = val_3\n"))
    env = Environments(None)
    env.load('')
    assert env._data == {"TEST_1": "val_1", "TEST_2": "val_2", "TEST_3": "val_3"}

