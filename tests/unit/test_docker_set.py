import os
import shutil
from unittest.mock import call

from dp_builder import const
from dp_builder.sets import DockerSet


def test_docker_set(settings_mock, requirements_mock, environment_mock, no_file_copy, no_cover, mocker, tmpdir):
    docker_set = DockerSet(settings_mock, requirements_mock, tmpdir, tmpdir)
    mocker.patch.object(docker_set, '_create_environment', return_value=environment_mock, autospec=True)
    docker_set.set()

    copy_calls = [
        call(os.path.join(const.TEMPLATES_DOCKER_DEV_PATH, "docker-compose.yml"), tmpdir),
        call(os.path.join(const.TEMPLATES_DOCKER_DEV_PATH, "Dockerfile"), os.path.join(tmpdir, const.APP_PATH)),
        call(os.path.join(const.TEMPLATES_DOCKER_DEV_PATH, "entrypoint.sh"), os.path.join(tmpdir, const.APP_PATH))
    ]
    shutil.copy.assert_has_calls(copy_calls, any_order=True)

    env_calls = [call(os.path.join(tmpdir, '.env.dev')), call(os.path.join(tmpdir, '.env.dev.db'))]
    environment_mock.save.assert_has_calls(env_calls, any_order=True)

    requirements_mock.add.assert_called_once_with('psycopg2-binary')

