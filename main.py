import urllib
import PyPDF2
from urllib.request import urlopen
from io import BytesIO
import urllib.error

DATA_URL = 'http://ww11.doh.state.fl.us/comm/_partners/covid19_report_archive/covid19-data/covid19_data_latest.pdf'


def open_url(url):
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


def str_to_int(array):
    """  Converts an array of comma seperated number-strings into a usable integer array.

    :param array: str array. Converts comma seperated number-strings into usable integers.
    :return: int array.
    """
    corrected_array = []

    for x in array:
        # Converting str to int then adding it to the array.
        corrected_array.append(int(x.replace(',', '')))

    return corrected_array


def print_data(array):
    """ Print function that displays the weekly COVID-19 statistics for Florida.

    :param array: An array of ints. Represents the weekly covid-19 stats. Index 1 = weekly numbers, index2 = cumulative.
    :return: None
    """
    print('==Total Covid-19 Cases==')
    print(f'Previous Week: {array[0]}')
    print(f'Cumulative: {array[1]}')


def main():
    # Getting our file via the provided URL.
    file = open_url(DATA_URL)

    # Creating a PDF reader object:
    pdfReader = PyPDF2.PdfFileReader(file)

    # Creating a page object based off the first page, then extracting the raw text:
    pageObj = pdfReader.getPage(0)
    raw_text = pageObj.extractText().split('\n') # Splitting our string at every new line into an array of strings.

    # Processing the raw text
    result = str_to_int(raw_text[13:15])

    # Printing our results:
    print_data(result)

    # Lastly, we close the PDF object:
    file.close()


if __name__ == "__main__":
    main()
