from dp_builder.sets import DjangoSet


def test_django_set(settings_mock):
    django_set = DjangoSet(settings_mock, 'test_app')
    django_set.set()
    settings_mock.extend_section.assert_called_once_with('INSTALLED_APPS', "'test_app'")


