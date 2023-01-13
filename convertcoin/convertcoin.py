from datetime import datetime, date

import requests
import argparse

API = "https://api.exchangerate.host/"
API_CURRENCIES = "https://api.exchangerate.host/symbols"

TODAY = {
    "today": datetime.today().strftime("%Y-%m-%d"),
    "year": int(datetime.today().strftime("%Y")),
    "month": int(datetime.today().strftime("%m")),
    "day": int(datetime.today().strftime("%d")),
}


def get_parameters():
    """Get parameters from user input to fetch API data."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_", action="store")
    parser.add_argument("--to", dest="to", action="store")
    parser.add_argument("--amount", dest="amount", action="store")
    parser.add_argument("--date", dest="date", action="store")
    args = parser.parse_args()

    return args


def get_accepted_currencies():

    list_ = []

    url = API_CURRENCIES
    response = requests.get(url)
    api_data = response.json()

    for key in api_data["symbols"]:
        list_.append(key)

    return list_


def validate_parameters(parameters):
    """Validate the parameters from user input."""

    # Assign parameters to shorter variables.
    from_ = parameters.from_
    to_ = parameters.to
    amount_ = parameters.amount
    date_ = parameters.date

    # Dictionary for data.
    data = {
        "valid": True,
        "message": "",
        "from": from_,
        "to":  to_,
        "amount": amount_,
        "date": date_
    }

    while True:

        # If amount is empty: Use 1.
        if amount_ is None:
            amount_ = "1"
            data["amount"] = amount_

        # Validate that amount is int or float.
        try:
            amount_ = int(amount_)
        except ValueError:
            try:
                amount_ = float(amount_)
            except ValueError:
                data["valid"] = False
                data["message"] = "Input error (amount). Please use only numbers and a floating point."
                break

        # If date is empty: Use today.
        if date_ is None:
            date_ = TODAY["today"]
            data["date"] = date_

        # Validate date input is correctly formatted and within accepted range.
        try:
            valid_date = datetime.strptime(date_, "%Y-%m-%d").date()
            if not (date(2000, 1, 1) <= valid_date <= (date(TODAY["year"], TODAY["month"], TODAY["day"]))):
                data["valid"] = False
                data["message"] = "Input error (date). Date not within accepted range."
                break
        except ValueError:
            data["valid"] = False
            data["message"] = "Input error (date). Date not accepted. Use format 2000-12-24."
            break

        break

    return data


def create_api_url(parameters):
    """Generate the full URL for API request from user parameters."""

    from_ = parameters["from"]
    to_ = parameters["to"]

    url = API + "convert?from=" + from_ + "&to=" + to_

    try:
        amount = parameters["amount"]
        url += "&amount=" + str(amount)
    except KeyError:
        pass

    try:
        date_ = parameters["date"]
        url += "&date=" + str(date_)
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
    data = validate_parameters(get_parameters())

    if data["valid"] is False:
        print(data["message"])

    else:

        # Generate the full URL for API request.
        url = create_api_url(data)

        # Get data from API.
        api_data = get_api_data(url)

        print(api_data)


if __name__ == "__main__":
    main()
