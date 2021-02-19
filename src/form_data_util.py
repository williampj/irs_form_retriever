from .utils.parser import parse_form_data
from .utils.form_summary import FormSummary
from .utils.irs_api import IRSApi
from .utils.input_error import InputError


class IRSFormData:
    def __init__(self, form_list):
        self.form_list = form_list

    # Validates the input and instantiates IRSFormData if valid
    def create(form_list):
        try:
            IRSFormData._validate_form_list(form_list)
            return IRSFormData(form_list)
        except InputError as e:
            InputError.handle_input_error(e)

    def request(self):
        form_summaries = []
        try:
            for form_name in self.form_list:
                matches = IRSApi(form_name).fetch_matches()
                form_summaries.append(parse_form_data(form_name, matches))
        except InputError as e:
            InputError.handle_input_error(e)
        return FormSummary.convert_to_json(form_summaries)

    # -------- Private methods ---------

    def _validate_form_list(form_list):
        if not isinstance(form_list, list):
            raise InputError("form list argument must be of type list")
        elif len(form_list) == 0:
            raise InputError("form list should not be empty")
        elif any(not isinstance(form, str) for form in form_list):
            raise InputError(
                "Every form in the form list must be of type string")
        else:
            return True
