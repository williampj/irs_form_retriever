class UI:
    def __init__(self, form_name, start_year, end_year):
        self.form_name = form_name
        self.start_year = start_year
        self.end_year = end_year

    def print_download_result(self, files_list):
        if len(files_list) > 0:
            print("The following documents were successfully downloaded:")
            print(('\n').join(files_list))
        elif self.start_year == self.end_year:
            print(
                f"No documents were found matching the name {self.form_name} for the year {self.start_year}")
        else:
            print(
                f"No documents were found matching the name {self.form_name} for the years {self.start_year}-{self.end_year}")
