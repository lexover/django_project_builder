import re
from typing import Union, List
from collections import namedtuple
from dp_builder.const import TAB


class PythonFileWorker:

    Section = namedtuple('Section', ('content', 'start', 'end', 'is_collection', 'variable_start'))

    def __init__(self):
        """
        This class allows you to load and process python files. Replace values for variables, expand collections,
        perform additional imports.
        """
        self._content: str = None

    def load(self, file_path: str) -> None:
        """
        Loads python file content from specified path
        :param file_path: the path to the file which be processed
        """
        with open(file_path, 'r') as file:
            self._content = file.read()

    def save(self, file_path):
        """
        Save content to specified file path.
        :param file_path: the path to the file.
        """
        with open(file_path, 'w') as file:
            file.write(self._content)

    def _match_to_section(self, match: re.Match) -> Section:
        if match is not None:
            start, end = match.regs[0]
            return self.Section(match[0], start, end)
        return None

    def _get_close_quote(self, open_quote):
        if open_quote == '[':
            return ']'
        elif open_quote == '{':
            return '}'
        elif open_quote == '(':
            return ')'
        return None

    def _find_close_quote(self, string, open_quote, position):
        """
        Search for close quote position ignoring all nested quotes.
        """
        close_quote = self._get_close_quote(open_quote)
        opened = 0
        for i, ch in enumerate(string[position:]):
            if ch == open_quote:
                opened += 1
            elif ch == close_quote:
                if opened != 0:
                    opened -= 1
                else:
                    return i + position

    def get_section(self, name: str):
        """
        Search for variable in file such as "value = 10" and return Section object in which specified variable
        declaration (Section.content), start and end position of section in file (Section.start, Section.end).
        :param variable_name: the variable name
        :return: the Section object with specified variable declaration, start and end position in file.
        """
        regex = f'({name}) *= *(.)(.*)\n'
        match = re.search(regex, self._content, flags=re.MULTILINE)
        if match is None:
            raise ValueError(f'Section with name {name} not found')
        is_collection = True if match[2] in '[{(' else False
        start, _ = match.regs[0]
        variable_position, _ = match.regs[2]
        if is_collection:
            end = self._find_close_quote(self._content, match[2], match.regs[2][1])
        else:
            end = match.regs[3][1] - 1
        return self.Section(self._content[start:end+1], start, end, is_collection, variable_position)

    def extend_section(self, section_name: str, rows: Union[str, List[str]], prepend: bool = False) -> None:
        """
        Extends the section by adding a new variable or variables specified in rows. By default new rows are added
        to the end of the collection. If prepend is True, then new rows will be added to the beginning of the collection
        :param section: section with collection
        :param rows: one string or array of new variables which will be added to the collection
        :param prepend: if True new variables is added to the beginning of the collection in other case to the end.
        """
        section = self.get_section(section_name)

        if type(rows) is not list:
            rows = [rows]

        if not section.is_collection:
            raise ValueError(f"Attempt to append data{rows} to variable, but only collection can be extended")

        start = section.variable_start
        end = section.end

        rows_str = []
        for row in rows:
            rows_str.append(f"{TAB}{row},\n")

        split_pos = start + 2 if prepend else end
        self._content = ''.join([self._content[:split_pos], ''.join(rows_str), self._content[split_pos:]])

    def replace_section(self, section_name: str, new_data: str) -> None:
        """
        Set new_data instead of specified section.
        :param section: the section that is being replaced
        :param new_data: the new data that will replace the section
        """
        section = self.get_section(section_name)
        self._content = ''.join([self._content[:section.start], new_data, self._content[section.end+1:]])

    def replace_value(self, section_name: str, new_value: str) -> None:
        """
        Set new_value the declaration will be the same `VAL = new_value`
        :param section: the section in which value will be set
        :param new_value: the new value that will be set for section
        """
        section = self.get_section(section_name)
        self._content = ''.join([self._content[:section.variable_start], new_value, self._content[section.end+1:]])

    def append_after(self, section_name: str, data: str) -> None:
        """
        Append the data after specified section.
        :param section: the section after which data will be added
        :param data: the added data
        """
        section = self.get_section(section_name)
        split_pos = section.end + 1
        self._content = ''.join([self._content[:split_pos], '\n', data, self._content[split_pos:]])

    def _find_last_import_position(self):
        last_import_pos = self._content.rindex('import')
        return self._content.find('\n', last_import_pos) + 1

    def add_import(self, import_val: str, from_val: str = None) -> None:
        """
        Add an `import import_val` if specified import_val only, or `from from_val import import_val` if specified
        both values. If module with data already in import it will be ignored.
        :param import_val: the value that sets after `import` keyword.
        :param from_val: the value that sets after `from` keyword
        """
        if from_val is None:
            import_str = f'import {import_val}\n'
        else:
            import_str = f'from {from_val} import {import_val}\n'
        if self._content.find(import_str) < 0:
            insert_pos = self._find_last_import_position()
            self._content = ''.join([self._content[:insert_pos], import_str, self._content[insert_pos:]])

    def __repr__(self):
        return self._content
