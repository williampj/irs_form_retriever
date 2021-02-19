from src.form_data_util import IRSFormData

# IRSFormData gatherer

# ------ uncomment following 3 lines to test --------
# forms = ['form w-2', 'Form 1095-C']
# json_result = IRSFormData.create(forms).request()
# print(json_result)
#
# =>
# [{"form_number": "Form W-2", "form_title": "Wage and Tax Statement (Info Copy Only)", "min_year": "1954", "max_year": "2021"}, {
#     "form_number": "Form 1095-C", "form_title": "Employer-Provided Health Insurance Offer and Coverage", "min_year": "2014", "max_year": "2020"}]
