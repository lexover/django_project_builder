import argparse
from dp_builder.cli import get_parameters
from dp_builder.project_builder import ProjectBuilder


def dp_builder():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', action='store', dest='project_name', help='help', default=None)
    parser.add_argument('-a', '--app', action='store', dest='app_name', help='help', default=None)
    args = parser.parse_args()

    parameters = get_parameters()
    builder = ProjectBuilder(args.project_name, args.app_name, parameters)
    builder.build()
