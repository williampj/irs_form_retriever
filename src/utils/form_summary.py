import json


class FormSummary:
    # class variable storing all FormSummary instances
    collection = []

    def __init__(self, form_number='', title='', year=''):
        self.form_number = form_number
        self.title = title
        self._assign_year(year)

    # class method that converts a collection of FormSummary instances to a single JSON object
    def convert_to_json(form_summaries):
        list = []
        for index in range(0, len(form_summaries)):
            list.append(form_summaries[index]._convert_to_dictionary())
        return json.dumps(list)

    def update_min_year(self, min_year):
        self.min_year = min_year

    # ------ Private Methods ------

    def _assign_year(self, year):
        self.max_year = year
        self.min_year = year

    def _convert_to_dictionary(self):
        return {
            "form_number": self.form_number,
            "form_title": self.title,
            "min_year": self.min_year,
            "max_year": self.max_year
        }
