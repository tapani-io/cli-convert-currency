# Convertcoin

A simple command-line tool to convert one currency into another. 

The program uses [ExchangeRate.host](https://exchangerate.host) API to fetch conversion rates. Currently it supports 171 currencies.

## Usage

    python3 convertcoin.py --from USD --to EUR --amount 12.34 --date 2020-12-24

**NOTE:** You can leave amount and date empty. Then the program will use 1 as amount and the date of today.