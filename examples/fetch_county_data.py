import CovidFL


def main():
    # Creating a parser object.
    parser = CovidFL.Parser()

    # Using our parse object to get a dictionary counting county data:
    county_data_dictionary = parser.fetch_county_data()

    # Printing our dictionary:
    print(county_data_dictionary)

    # printing just Leon county's data -- note county names have to start with a capital letter
    leon_data = county_data_dictionary['Leon']
    print(leon_data)


if __name__ == "__main__":
    main()
