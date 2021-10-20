import CovidFL



def main():
    # Creating a parser object.
    parser = CovidFL.Parser()

    # Using our parser object to fetch data from the PDF's tables:
    table_data_dictionary = parser.fetch_table_data()

    # Fetching just the 'Vaccine age groups' table as a dictionary:
    vaccine_age_groups_data = table_data_dictionary['vaccine-age-groups']

    # Printing the dictionary contain "Vaccine age groups" data:
    print(vaccine_age_groups_data)






if __name__ == "__main__":
    main()
