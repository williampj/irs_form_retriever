# IRS Form Retriever

The IRS Form retriever contains two utilities, one for downloading IRS forms (`form_download.py`) and one for gathering data on a list of IRS forms (`form_data.py`).

## Requirements

- Python 3.9.1
- Downloaded packages:
  - grequests==0.6.0
  - requests-html==0.10.0
- The package list stored in `requirements.txt`

## form_data.py

The `form_data.py` file is used to gather information on specific IRS tax forms. It imports the IRSFormData class from the form_data_util utility file. Alternatively, any file can import the`IRSFormData`class from the`src/form_data_util.py` file and apply it.

#### Usage

To instantiate the `IRSFormData`, call the `IRSFormData.create` class method and pass the following argument:
`forms`: list of strings

The `forms` argument must consist of a list of strings corresponding to the requested form names. Each form name is case insensitive, matching a lower cased form name with lower cased forms on the IRS homepage.

To request the forms data, call `request()` on the instance returned from the `IRSFormData.create` method call.

```py
json_result = IRSFormData.create(forms).request()
```

A JSON object will be returned with the following format:

```json
{
  "form_number": "",
  "form_title": "",
  "min_year": "",
  "max_year": ""
}
```

## form_download.py

The `form_download.py` file is used to download IRS tax forms.
It imports the `IRSFormDownloader` class from the `form_download_util` utility file.

Alternatively, any file can import the `IRSFormDownloader` class from the `src/form_download_util.py` file and apply it.

#### Usage

To instantiate the `IRSFormDownloader`, call the `IRSFormDownloader.create` class method and pass pass the following arguments:
`form`: string
`starting year`: integer
`ending year`(opt): integer

The `form` argument is case insensitive, matching a lower cased version of the string with lower cased forms on the IRS homepage.
When downloading files to a folder, the folder and file names are titleized, so for instance
`FoRm w-2` will download `Form W-2` files to a `./Form W-2` folder.

`ending year` is optional. If it is omitted, only a form for a single year (the `starting year`) will be requested. If the ending year is set earlier or equal to the `starting year`, then the `starting year` will likewise be the only year requested.

To download the forms, call `download()` on the instance returned from the `IRSFormDownloader.create` method call.

```py
IRSFormDownloader.create(form, start_year, end_year).download()
```

## Testing

Tests were run using `pytest`.
Running `pytest test.py` runs a test suite seven passing tests.
