import os

this_dir, this_filename = os.path.split(__file__)

ROOT_PATH = os.getcwd()
TESTS_PATH = os.path.join(ROOT_PATH, "tests", "")

TEMPLATES_PATH = os.path.join(this_dir, "templates")
TEMPLATES_DOCKER_DEV_PATH = os.path.join(TEMPLATES_PATH, "Docker", "dev")
TEMPLATES_DOCKER_PROD_PATH = os.path.join(TEMPLATES_PATH, "Docker", "prod")

APP_PATH = 'app'
TAB = ' ' * 4
