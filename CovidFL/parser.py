import time
import urllib
import PyPDF4
from urllib.request import urlopen
from io import BytesIO
import urllib.error
import bs4
import requests
import lxml



def fetch_data_urls(reverse=True):
    url = 'http://ww11.doh.state.fl.us/comm/_partners/covid19_report_archive/covid19-data/'
    r = requests.get(url)

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    tags = soup.find_all("a")[5:]

    links = []
    for x in tags:
        links.append('http://ww11.doh.state.fl.us/comm/_partners/covid19_report_archive/covid19-data/' + x.get('href'))

    if reverse is True:
        links.reverse()

    return links


class Parser:

    def __init__(self, url='http://ww11.doh.state.fl.us/comm/_partners/covid19_report_archive/covid19-data/covid19_data_latest.pdf'):
        self.data_url = url

    def __open_url(self, url):
        """ Create a byte stream for the provided URL.
        This is like `open(filename, 'rb')` except, we don't need to have the file locally stored, we just
        grab the bytes via a get-request to the URL.

        :param url: The URL we wish to pull the file from.
        :return: `io.BytesIO()`. A stream containing the bytes from the file that is located at the URL.
        """

        http_response = ''
        try:
            http_response = urllib.request.urlopen(url)
        except urllib.error.URLError:
            Exception('COVID-PDF: Error fetching the URL')

        return BytesIO(http_response.read())

    def __str_to_int(self, array):
        """  Converts an array of comma seperated number-strings into a usable integer array.

        :param array: str array. Converts comma seperated number-strings into usable integers.
        :return: int array.
        """
        corrected_array = []

        for x in array:
            # Converting str to int then adding it to the array.
            corrected_array.append(int(x.replace(',', '')))

        return corrected_array


    def fetch_table_data(self):
        """ Fetches the latest weekly COVID-19 data for Florida.

        :return: dict. A dictionary containing data parsed from Florida Health's COVID-19 Weekly Situation report
        """

        # Creating the dictionary that will store out parsed data:
        results = {
            'case-data':
                {
                    'total': {'previous-week': None, 'cumulative': None},
                    'new-case-positivity': {'previous-week': None, 'cumulative': None},
                    'deaths': {'previous-week': None, 'cumulative': None}
                },
            'vaccine-data':
                {
                    'total': {'previous-week': None, 'cumulative': None},
                    'first-dose': {'previous-week': None, 'cumulative': None},
                    'series-completed': {'previous-week': None, 'cumulative': None},
                    'additional-dose': {'previous-week': None, 'cumulative': None}
                },
            'vaccine-age-groups':
                {
                    'total': {'population': None, 'vaccinated': None},
                    '12-19': {'population': None, 'vaccinated': None},
                    '20-29': {'population': None, 'vaccinated': None},
                    '30-39': {'population': None, 'vaccinated': None},
                    '40-49': {'population': None, 'vaccinated': None},
                    '50-59': {'population': None, 'vaccinated': None},
                    '60-64': {'population': None, 'vaccinated': None},
                    '65+': {'population': None, 'vaccinated': None},
                },
        }

        # TODO: Instead of reassigning values into a dictionary, perhaps just initially assigning our parsed data?
        #       This would make the code cleaner, but perhaps harder to maintain.

        file = self.__open_url(self.data_url)

        # Creating a PDF reader object:
        pdfReader = PyPDF4.PdfFileReader(file)



        # Creating a page object based off the first page, then extracting the raw text:
        pageObj = pdfReader.getPage(0)
        raw_text = pageObj.extractText().split('\n')  # Splitting our string at every new line into an array of strings.

        # Parsing out data from the 'Case data' table and storing it in our dictionary:
        results['case-data']['total']['previous-week'] = raw_text[13]
        results['case-data']['total']['cumulative'] = raw_text[14]
        results['case-data']['new-case-positivity']['previous-week'] = raw_text[19]
        results['case-data']['new-case-positivity']['cumulative'] = raw_text[20]
        results['case-data']['deaths']['previous-week'] = raw_text[25]
        results['case-data']['deaths']['cumulative'] = raw_text[26]

        # Parsing out data from 'Vaccine data' table and storing it on our dictionary:
        results['vaccine-data']['total']['previous-week'] = raw_text[16]
        results['vaccine-data']['total']['cumulative'] = raw_text[17]
        results['vaccine-data']['first-dose']['previous-week'] = raw_text[22]
        results['vaccine-data']['first-dose']['cumulative'] = raw_text[23]
        results['vaccine-data']['series-completed']['previous-week'] = raw_text[28]
        results['vaccine-data']['series-completed']['cumulative'] = raw_text[29]
        results['vaccine-data']['additional-dose']['previous-week'] = raw_text[31]
        results['vaccine-data']['additional-dose']['cumulative'] = raw_text[32]

        # Parsing out data from the 'Vaccine age groups' table and storing it in our dictionary:
        results['vaccine-age-groups']['total']['population'] = raw_text[37]
        results['vaccine-age-groups']['total']['vaccinated'] = raw_text[38]
        results['vaccine-age-groups']['12-19']['population'] = raw_text[40]
        results['vaccine-age-groups']['12-19']['vaccinated'] = raw_text[41]
        results['vaccine-age-groups']['20-29']['population'] = raw_text[43]
        results['vaccine-age-groups']['20-29']['vaccinated'] = raw_text[44]
        results['vaccine-age-groups']['30-39']['population'] = raw_text[46]
        results['vaccine-age-groups']['30-39']['vaccinated'] = raw_text[47]
        results['vaccine-age-groups']['40-49']['population'] = raw_text[49]
        results['vaccine-age-groups']['40-49']['vaccinated'] = raw_text[50]
        results['vaccine-age-groups']['50-59']['population'] = raw_text[52]
        results['vaccine-age-groups']['50-59']['vaccinated'] = raw_text[53]
        results['vaccine-age-groups']['60-64']['population'] = raw_text[55]
        results['vaccine-age-groups']['60-64']['vaccinated'] = raw_text[56]
        results['vaccine-age-groups']['65+']['population'] = raw_text[58]
        results['vaccine-age-groups']['65+']['vaccinated'] = raw_text[59]

        # Lastly, we close the PDF object:
        file.close()

        return results

    def __parse_county_page(self, page_number: int, pdfReader):
        new_array = []

        # Creating a page object based off the first page, then extracting the raw text:
        pageObj = pdfReader.getPage(page_number - 1)
        print(pageObj.extractText())
        raw_text = pageObj.extractText().split('\n')  # Splitting our string at every new line into an array of strings.

        # Filtering out whitespace from our result
        if page_number == 4:
            new_array = list(filter(str.strip, raw_text))[20:-5]
        elif page_number == 5:
            new_array = list(filter(str.strip, raw_text))[24:-1]
        elif page_number == 6:
            # Page 6 has some descepancies in the formatting. We are basically cutting out the 'unknown' county to
            # deal with this
            new_array = list(filter(str.strip, raw_text))[24:-48] + list(filter(str.strip, raw_text))[-41:-1]
        else:
            Exception("COVID PDF: Invalid page provided for county page parsing.")

        return new_array

    def fetch_county_data(self):
        # Getting our file via the provided URL.
        file = self.__open_url(self.data_url)

        # Creating a PDF reader object:
        pdfReader = PyPDF4.PdfFileReader(file)

        info = pdfReader.getDocumentInfo()


        # Fetching the raw text from each page and combining it into one array:
        raw_text = self.__parse_county_page(4, pdfReader) \
                   + self.__parse_county_page(5, pdfReader) \
                   + self.__parse_county_page(6, pdfReader)

        results = {}

        for x, y in enumerate(raw_text):
            if x % 10 == 0: # Every 10 elements is new county info
                results[y] = {}
                results[y]['2021-population'] = raw_text[x + 1]
                results[y]['cumulative'] = {'people-vaccinated': raw_text[x + 2],
                                            'percent-12+-vaccinated': raw_text[x + 3],
                                            'cases': raw_text[x + 4],
                                            'new-case-positivity': raw_text[x + 5]
                                            }
                results[y]['previous-week'] = {'people-vaccinated': raw_text[x + 6],
                                               'cases': raw_text[x + 7],
                                               'new-case-positivity': raw_text[x + 8],
                                               'cases-per-100,000-population': raw_text[x + 9]
                                               }
            #time.sleep(6) # sleep for 6 seconds so we don't flood Florida's DOH's servers

        # Lastly, we close the PDF object:
        file.close()

        return results

    def fetch_all_data(self):
        county_data = self.fetch_county_data()
        table_data = self.fetch_table_data()
        return dict(county_data, **table_data)
