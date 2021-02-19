from .utils.file_manager import FileManager
from .utils.irs_api import IRSApi
from .utils.parser import parse_range
from .utils.user_interface import UI
from .utils.input_error import InputError


class IRSFormDownloader:
    def __init__(self, form_name, start_year, end_year=0):
        self.form_name = form_name
        self._assign_years(start_year, end_year)
        self.irs_api = IRSApi(form_name)
        self.ui = UI(form_name, self.start_year, self.end_year)

    # Validates the input and instantiates IRSFormDownloader if valid
    def create(form_name, start_year, end_year=0):
        try:
            IRSFormDownloader._validate_form_name(form_name)
            IRSFormDownloader._validate_years(start_year, end_year)
            return IRSFormDownloader(form_name.title(), start_year, end_year)
        except InputError as e:
            InputError.handle_input_error(e)

    def download(self):
        matches = self.irs_api.fetch_matches()
        if matches:
            matches_range = parse_range(
                matches, self.form_name, self.start_year, self.end_year)
            files_downloaded = self.irs_api.download_matches(matches_range)
        self.ui.print_download_result(files_downloaded)

    def _validate_form_name(form_name):
        if not isinstance(form_name, str):
            raise InputError('form argument must be of type string')
        return True

    def _validate_years(start_year, end_year):
        if not isinstance(start_year, int):
            raise InputError('start year argument must be of type integer')
        if not isinstance(end_year, int):
            raise InputError('end year argument must be of type integer')
        return True

    def _assign_years(self, start_year, end_year):
        if start_year > end_year:
            end_year = start_year
        self.start_year = start_year
        self.end_year = end_year
