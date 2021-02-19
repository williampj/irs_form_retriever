import os
import re


class FileManager:
    def __init__(self, form_name):
        self.form_name = form_name

    files_downloaded = []

    def create_folder(self):
        os.makedirs(f"./{self.form_name}", exist_ok=True)

    def create_files(self, response_objects):
        for response_object in response_objects:
            self._create_file(response_object)

    # ------ Private Methods ------

    def _create_file(self, response_object):
        file_name = self._generate_file_name(response_object)
        with open(file_name, 'wb') as file:
            file.write(response_object.content)
            self.files_downloaded.append(file_name)

    def _generate_file_name(self, response_object):
        year = self._extract_year(response_object)
        return f"./{self.form_name}/{self.form_name} - {year}.pdf"

    def _extract_year(self, response_object):
        # lookbehind of "--" and lookahead of ".pdf"
        pattern = '(?<=--)[0-9]{4}(?=.pdf)'
        url = response_object.url
        return re.search(pattern, url).group(0)
