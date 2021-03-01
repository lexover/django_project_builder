from dp_builder.const import TAB
from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.requirements import Requirements
from dp_builder.sets import AbstractSet


class DrfSet(AbstractSet):
    def __init__(self,
                 requirements: Requirements,
                 settings: PythonFileWorker,
                 urls: PythonFileWorker,
                 version=None):
        self.requirements = requirements
        self.settings = settings
        self.version = version
        self.urls = urls

    section = ''.join([
        "\nREST_FRAMEWORK = {\n",
        f"{TAB}'TEST_REQUEST_DEFAULT_FORMAT': 'json',\n",
        "}"
    ])

    def set(self):
        self.requirements.add('djangorestframework')

        self.settings.extend_section('INSTALLED_APPS', f"'rest_framework'")
        self.settings.append_after('WSGI_APPLICATION', self.section)

        self.urls.add_import(from_val='django.urls', import_val='path')
        self.urls.add_import(from_val='django.urls', import_val='include')
        self.urls.extend_section('urlpatterns', f"path('api-auth/', include('rest_framework.urls'))")
