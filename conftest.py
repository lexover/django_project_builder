import pytest
from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.environments import Environments
from dp_builder.requirements import Requirements


@pytest.fixture()
def settings_mock(mocker):
    settings = PythonFileWorker()
    mocker.patch.object(settings, 'extend_section', autospec=True)
    mocker.patch.object(settings, 'replace_section', autospec=True)
    mocker.patch.object(settings, 'replace_value', autospec=True)
    mocker.patch.object(settings, 'append_after', autospec=True)
    mocker.patch.object(settings, 'add_import', autospec=True)
    mocker.patch.object(settings, 'save', autospec=True)
    return settings


@pytest.fixture()
def environment_mock(settings_mock, mocker):
    env = Environments(settings_mock)
    mocker.patch.object(env, 'set', autospec=True)
    mocker.patch.object(env, 'bind_to_setting', autospec=True)
    mocker.patch.object(env, 'save', autospec=True)
    return env


@pytest.fixture()
def requirements_mock(mocker):
    requirements = Requirements()
    mocker.patch.object(requirements, 'add', autospec=True)
    mocker.patch.object(requirements, 'save', autospec=True)
    return requirements


@pytest.fixture()
def no_file_copy(mocker):
    mocker.patch('shutil.copy')
