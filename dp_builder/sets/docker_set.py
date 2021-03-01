import os
import shutil

from dp_builder.const import TEMPLATES_DOCKER_DEV_PATH, APP_PATH
from dp_builder.environments import Environments
from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.requirements import Requirements
from dp_builder.sets import AbstractSet
from dp_builder.utils import generate_random_string

db_section = \
    """DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'db'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}"""


class DockerSet(AbstractSet):

    allowed_hosts = ["localhost", "127.0.0.1", "[::1]"]

    def __init__(self,
                 settings: PythonFileWorker,
                 requirements: Requirements,
                 project_path: str,
                 project_name: str,
                 db_name: str = 'django_dev',
                 db_user: str = 'db_user',
                 db_password: str = 'db_password'):
        self.settings = settings
        self.requirements = requirements
        self.project_path = project_path
        self.project_name = project_name
        self.db_engine = 'django.db.backends.postgresql'
        self.db_host = 'db'
        self.db_port = '5432'
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def _create_environment(self, settings):
        return Environments(settings)

    def set(self):

        # Here used Postgres which need a driver for Django psycopg2 we have to add it to requirements
        self.requirements.add('psycopg2-binary')

        # Copy docker-compose.yml from template to PROJECT_ROOT
        shutil.copy(os.path.join(TEMPLATES_DOCKER_DEV_PATH, 'docker-compose.yml'), self.project_path)

        # Copy .env from template to PROJECT_ROOT
        main_env = self._create_environment(self.settings)
        db_dev_env = self._create_environment(self.settings)

        # Create new section for database
        self.settings.replace_section("DATABASES", db_section)
        # Create .env.dev and bind it with settings
        main_env.bind_to_setting('SECRET_KEY', value=generate_random_string(12))
        main_env.bind_to_setting('DEBUG', value=1, default=0)
        main_env.bind_to_setting('ALLOWED_HOSTS', value=self.allowed_hosts, default=self.allowed_hosts)
        main_env.set("SQL_ENGINE", self.db_engine)
        main_env.set("SQL_DATABASE", self.db_name)
        main_env.set("SQL_USER", self.db_user)
        main_env.set("SQL_PASSWORD", self.db_password)
        main_env.set("SQL_HOST", self.db_host)
        main_env.set("SQL_PORT", self.db_port)

        # Create .env.dev.db to configure Postgres
        db_dev_env.set("POSTGRES_DB", self.db_name)
        db_dev_env.set("POSTGRES_USER", self.db_user)
        db_dev_env.set("POSTGRES_PASSWORD", self.db_password)

        main_env.save(os.path.join(self.project_path, '.env.dev'))
        db_dev_env.save(os.path.join(self.project_path, '.env.dev.db'))

        # Copy Dockerfile from template to PROJECT_ROOT/app
        app_path = os.path.join(self.project_path, APP_PATH)
        shutil.copy(os.path.join(TEMPLATES_DOCKER_DEV_PATH, 'Dockerfile'), app_path)
        # Copy entrypoint from template to PROJECT_ROOT/app
        shutil.copy(os.path.join(TEMPLATES_DOCKER_DEV_PATH, 'entrypoint.sh'), app_path)
