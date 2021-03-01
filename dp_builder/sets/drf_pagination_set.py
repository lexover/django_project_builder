from dp_builder.sets import AbstractSet
from dp_builder.pythons_file_worker import PythonFileWorker


class DrfPaginationSet(AbstractSet):
    def __init__(self, settings: PythonFileWorker, page_size):
        self.settings = settings
        self.page_size = page_size

    pagination_class = "'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'"

    def page_size_section(self):
        return f"'PAGE_SIZE': {self.page_size}"

    def set(self):
        self.settings.extend_section('REST_FRAMEWORK', [self.pagination_class, self.page_size_section()])
