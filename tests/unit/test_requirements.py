import builtins

import pytest

from dp_builder.requirements import Requirements


@pytest.fixture
def requirements():
    return Requirements()


@pytest.mark.parametrize(
    'version, expected',
    [
        ('0.0.1', True),
        ('10.21.34', True),
        ('21.23', False),
        ('adb', False),
        ('a.1.3', False),
    ]
)
def test_validate_version(version, expected, requirements):
    assert requirements.validate_version(version) == expected


def test_add_valid(requirements):
    requirements.add('package_1', '0.1.1')
    requirements.add('package_2', '0.1.1')
    requirements.add('package_3')
    assert len(requirements._data) == 3


def test_add_error_incorrect_version(requirements):
    with pytest.raises(ValueError) as err:
        requirements.add('package', 'abc')
        assert err.value == 'Specified package `package==abc` version incorrect'


def test_add_error_dublicate_package(requirements):
    with pytest.raises(ValueError) as err:
        requirements.add('package', '0.1.1')
        requirements.add('package', '0.1.1')
        assert err.value == 'Package with name `package` already in requirements'


def test_save_requirements(requirements, mocker):
    mocker.patch('builtins.open', autospec=True)
    requirements._data = [
        requirements.Package('test_1', '0.0.1'),
        requirements.Package('test_2', None)
    ]
    expected = 'test_1==0.0.1\ntest_2\n'
    requirements.save('here')
    builtins.open.assert_called_once_with('here', 'w')
    handle = builtins.open.return_value.__enter__.return_value
    handle.write.assert_called_once_with(expected)
