import os
from typing import Dict, Any

from dp_builder import sets
from dp_builder.const import ROOT_PATH, APP_PATH
from dp_builder.pythons_file_worker import PythonFileWorker
from dp_builder.requirements import Requirements


class ProjectBuilder:
    def __init__(self, project_name: str, app_name: str, params: Dict[str, Any]):
        self.project_name = project_name
        self.app_name = app_name
        self.params = params
        self.sets_list = []

        self.root_path = os.path.join(ROOT_PATH, project_name)
        self.project_path = os.path.join(self.root_path, APP_PATH, project_name)
        self.settings_path = os.path.join(self.project_path, 'settings.py')
        self.urls_path = os.path.join(self.project_path, 'urls.py')

    def _load_settings(self) -> PythonFileWorker:
        settings = PythonFileWorker()
        settings.load(self.settings_path)
        return settings

    def _load_urls(self) -> PythonFileWorker:
        urls = PythonFileWorker()
        urls.load(self.urls_path)
        return urls

    def _create_requirements(self) -> Requirements:
        return Requirements()

    def build(self) -> None:
        # Load settings.py from project
        settings = self._load_settings()
        # Create requirements.txt
        requirements = self._create_requirements()
        # Load urls.py from project
        urls = self._load_urls()

        if 'drf' in self.params['main']:
            self.sets_list.append(sets.DrfSet(requirements, settings, urls))
            if 'paging' in self.params['drf']:
                self.sets_list.append(sets.DrfPaginationSet(settings, 10))
            if 'simplejwt' in self.params['drf']:
                self.sets_list.append(sets.DrfSimpleJwtSet(requirements, settings, urls))
        self.sets_list.append(sets.DjangoSet(settings, self.app_name))
        if 'docker' in self.params['main']:
            if 'db' in self.params:
                db_param = self.params["db"]
                docker_set = sets.DockerSet(settings,
                                            requirements,
                                            self.root_path,
                                            self.project_name,
                                            db_name=db_param["db_name"],
                                            db_user=db_param["db_user"],
                                            db_password=db_param["db_password"])
            else:
                docker_set = sets.DockerSet(settings, requirements, self.root_path, self.project_name)
            self.sets_list.append(docker_set)

        # Apply every set in sets_list (build project)
        [item.set() for item in self.sets_list]

        # Save changed files
        requirements.save(os.path.join(self.root_path, APP_PATH, 'requirements.txt'))
        settings.save(self.settings_path)
        urls.save(self.urls_path)
