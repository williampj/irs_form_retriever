from os import path
from src.form_data_util import IRSFormData
from src.form_download_util import IRSFormDownloader
import json
import shutil


def test_form_data_util_with_valid_input():
    form_list = ['Form W-2', 'Form 1095-C']
    irs_fd = IRSFormData.create(form_list)
    result = irs_fd.request()
    assert result == json.dumps([{'form_number': 'Form W-2', 'form_title': 'Wage and Tax Statement (Info Copy Only)',
                                  'min_year': '1954', 'max_year': '2021'}, {'form_number': 'Form 1095-C', 'form_title': 'Employer-Provided Health Insurance Offer and Coverage', 'min_year': '2014', 'max_year': '2020'}])


def test_form_data_util_with_invalid_input_format(capsys):
    # IRSFormData.create method returns None and prints error message if input is invalid
    form_list = 'not a list'
    irs_fd = IRSFormData.create(form_list)
    out, _ = capsys.readouterr()
    # Prints InputError if input is invalid
    assert out == 'InputError: form list argument must be of type list\n'
    # Returns None if input is invalid
    assert irs_fd == None


def test_form_data_util_with_invalid_input_empty_list(capsys):
    # IRSFormData.create method returns None and prints error message if input is invalid
    form_list = []
    irs_fd = IRSFormData.create(form_list)
    out, _ = capsys.readouterr()
    # Prints InputError if input is invalid
    assert out == 'InputError: form list should not be empty\n'
    # Returns None if input is invalid
    assert irs_fd == None


def test_download_form_util_with_valid_input_range():
    form = 'Form W-2'
    start_year = 2004
    end_year = 2006
    irs = IRSFormDownloader.create(form, start_year, end_year)
    irs.download()

    assert path.exists('./Form W-2/Form W-2 - 2004.pdf')
    assert path.exists('./Form W-2/Form W-2 - 2005.pdf')
    assert path.exists('./Form W-2/Form W-2 - 2006.pdf')
    shutil.rmtree('./Form W-2')


def test_download_form_util_with_valid_input_single_year():
    form = 'Form W-2'
    start_year = 1996
    irs = IRSFormDownloader.create(form, start_year)
    irs.download()

    assert path.exists('./Form W-2/Form W-2 - 1996.pdf')
    shutil.rmtree('./Form W-2')


def test_download_form_util_with_invalid_form_input(capsys):
    form = 99999
    start_year = 1996
    end_year = 2006
    irs = IRSFormDownloader.create(form, start_year, end_year)
    out, _ = capsys.readouterr()
    # Prints InputError if input is invalid
    assert out == 'InputError: form argument must be of type string\n'
    # Returns None if input is invalid
    assert irs == None


def test_download_form_util_with_invalid_year_input(capsys):
    form = 'Form W-2'
    start_year = 'invalid year'
    end_year = 2006
    irs = IRSFormDownloader.create(form, start_year, end_year)
    out, _ = capsys.readouterr()
    # Prints InputError if input is invalid
    assert out == 'InputError: start year argument must be of type integer\n'
    # Returns None if input is invalid
    assert irs == None
