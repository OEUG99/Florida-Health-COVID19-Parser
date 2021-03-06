import CovidFL
from CovidFL import fetch_data_urls


def main():
    """
    Note: Using previous week PDF's is not guaranteed to work, as older weeks have slightly different PDF formats.
            Weeks close in range should work, as long as they are some what recent. This is an experimental
            implementation, use at your own risk.
    """

    # Using a previous week's PDF ** index 0 is the current week, index 1 is one week ago,
    # index n is n weeks ago.
    custom_url = fetch_data_urls()[1]
    print(custom_url)

    # Creating a parser object with keyword argument url
    parser = CovidFL.Parser(url=custom_url)

    # Using our parser object to fetch data from the PDF's tables:
    table_data_dictionary = parser.fetch_table_data()

    # Fetching just the 'Vaccine age groups' table as a dictionary:
    vaccine_age_groups_data = table_data_dictionary['vaccine-age-groups']

    # Printing the dictionary contain "Vaccine age groups" data:
    print(vaccine_age_groups_data)


if __name__ == "__main__":
    main()
