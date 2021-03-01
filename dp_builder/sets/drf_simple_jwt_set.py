from dp_builder.const import TAB
from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.requirements import Requirements
from dp_builder.sets import AbstractSet


class DrfSimpleJwtSet(AbstractSet):
    def __init__(self, requirements: Requirements, settings: PythonFileWorker, urls: PythonFileWorker, version=None):
        self.requirements = requirements
        self.settings = settings
        self.version = version
        self.urls = urls

    auth_classes_start = "'DEFAULT_AUTHENTICATION_CLASSES': (\n"
    auth_classes_content = f"'rest_framework_simplejwt.authentication.JWTAuthentication',\n"
    auth_classes_end = f")"

    url_token = f"path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair')"
    url_refresh = f"path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')"
    url_verify = f"path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')"

    def auth_classes_section(self):
        return ''.join([
            f'{self.auth_classes_start}',
            f'{TAB}{TAB}{self.auth_classes_content}',
            f'{TAB}{self.auth_classes_end}'
        ])

    def set(self):
        self.requirements.add("djangorestframework-simplejwt")

        self.settings.extend_section("REST_FRAMEWORK", self.auth_classes_section())

        self.urls.add_import(import_val="TokenObtainPairView", from_val="rest_framework_simplejwt.views")
        self.urls.add_import(import_val="TokenRefreshView", from_val="rest_framework_simplejwt.views")
        self.urls.add_import(import_val="TokenVerifyView", from_val="rest_framework_simplejwt.views")
        self.urls.extend_section("urlpatterns", [self.url_token, self.url_refresh, self.url_verify])
