import requests
import argparse

API = "https://api.exchangerate.host/"


def get_parameters():
    """Get parameters from user input to fetch API data."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_", action="store")
    parser.add_argument("--to", dest="to", action="store")
    parser.add_argument("--amount", dest="amount", action="store")
    parser.add_argument("--date", dest="date", action="store")
    args = parser.parse_args()

    return args


def validate_parameters(parameters):
    """Validate the parameters from user input."""

    # Assign parameters to shorter variables.
    from_ = parameters.from_
    to = parameters.to
    amount = parameters.amount
    date = parameters.date

    while True:

        # If amount is empty: Use 1.
        if amount is None:
            amount = "1"

        # Validate that amount is int or float.
        try:
            amount = int(amount)
        except ValueError:
            try:
                amount = float(amount)
            except ValueError:
                valid = False
                break

        data = {
            "from": from_,
            "to": to,
            "amount": amount,
            "date": date
        }
        return data

    if valid is False:
        return "Not valid"


def create_api_url(parameters):
    """Generate the full URL for API request from user parameters."""

    from_ = parameters["from"]
    to = parameters["to"]

    url = API + "convert?from=" + from_ + "&to=" + to

    try:
        amount = parameters["amount"]
        url += "&amount=" + str(amount)
    except KeyError:
        pass

    try:
        date = parameters["date"]
        url += "&date=" + str(date)
    except KeyError:
        pass

    return url


def get_api_data(url):
    """Get data from API."""

    response = requests.get(url)
    api_data = response.json()
    pretty_data = str(api_data["query"]["amount"]) + " " + api_data["query"]["from"] + " is " + str(
        api_data["result"]) + " " + api_data["query"]["to"] + " on " + api_data["date"]

    return pretty_data


def main():

    # Get parameters for API request from user input and validate it.
    parameters = validate_parameters(get_parameters())

    if parameters == "Not valid":
        print("Input not valid. Try again.")

    else:

        # Generate the full URL for API request.
        url = create_api_url(parameters)

        # Get data from API.
        api_data = get_api_data(url)

        print(api_data)


if __name__ == "__main__":
    main()
