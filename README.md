# cli-convert-currency

A very simple command-line program to convert one currency into another. 

The program uses [ExchangeRate.host](https://exchangerate.host) API for fetching conversion rates.

## usage

    python3 cli-convert-currency.py --from usd --to eur --amount 10 --date 2020-12-24

**NOTE:** You can leave amount and date empty. Then the program will use 1 as amount and todays date.
