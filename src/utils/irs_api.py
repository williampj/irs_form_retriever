import grequests
from requests_html import HTMLSession
from .file_manager import FileManager
session = HTMLSession()


class IRSApi:
    def __init__(self, form_name):
        self.form_name = form_name

    def fetch_matches(self):
        self._generate_url_query()
        return self._get_page_results()

    def download_matches(self, matches):
        # Maps HTML table row matches to a list of urls
        def map_matches_to_urls():
            return list(map(lambda match: match.find('a')[0].attrs['href'], matches))

        # Number of asynchronous http requests
        BATCH_LENGTH = 5
        files_downloaded = []

        file_manager = FileManager(self.form_name)
        file_manager.create_folder()
        urls = map_matches_to_urls()

        # Processes 5 asynchronous http requests per loop
        while urls:
            batch = urls[:BATCH_LENGTH]
            responses = (grequests.get(url) for url in batch)
            batch_results = grequests.map(responses)
            files_downloaded += batch_results
            urls = urls[BATCH_LENGTH:]

        file_manager.create_files(files_downloaded)
        return file_manager.files_downloaded

        # -------- Private Methods --------

    def _generate_url_query(self):
        url_encoded_form_name = self.form_name.strip().replace(' ', '+')
        self.url_query = f"?value={url_encoded_form_name}&criteria=formNumber&submitSearch=Find"

    def _get_page_results(self):
        BASE_URL = "https://apps.irs.gov"
        PATH = "/app/picklist/list/priorFormPublication.html"
        TABLE_ROW_SELECTOR = '.picklist-dataTable > tr'

        # HTTP request to the IRS form publications page
        self.page = session.get(BASE_URL + PATH + self.url_query)
        if self._no_matches():
            return []
        pagination_link = self._get_pagination_link()
        # Issues http request for the pagination link to collect all matches in one HTML page
        # and then return the matching table rows
        return session.get(BASE_URL + pagination_link).html.find(TABLE_ROW_SELECTOR)[1:]

    def _no_matches(self):
        RESULTS_TABLE = 'th.NumResultsDisplayed'
        return len(self.page.html.find(RESULTS_TABLE)) == 0

    def _get_pagination_link(self):
        # SELECTORS
        ONE_HUNDRED_RESULTS = 'th.NumResultsDisplayed > a:nth-child(3)'
        TWO_HUNDRED_RESULTS = 'th.NumResultsDisplayed > a:nth-child(4)'
        # These three forms have existed for over 100 years, thus requiring a listing of 200 results
        HISTORICAL_FORMS = ['1040', '1041', '1120']

        is_historical_form = len(
            list(filter(lambda x: (x in self.form_name), HISTORICAL_FORMS))) > 0
        if is_historical_form:
            # Returns 200 results for forms 1040, 1041, 1120
            return self.page.html.find(TWO_HUNDRED_RESULTS)[0].attrs['href']
        else:
            # Returns 100 results for newer forms (all other than 1040, 1041, 1120)
            return self.page.html.find(ONE_HUNDRED_RESULTS)[0].attrs['href']
