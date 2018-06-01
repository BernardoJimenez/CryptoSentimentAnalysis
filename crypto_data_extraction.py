# requests library used to make HTTP calls
import requests
# write/read JavaScript Object Notation
import json

'''
# Using CryptoCompare site's API: https://min-api.cryptocompare.com
# use 'Historical Daily OHLCV' API Historical Data section
BTC_data_url = 'https://min-api.cryptocompare.com/data/histoday'
# extract data from April 30th to June 1st 2018
url_params = {'fsym': 'BTC', 'tsym': 'USD', 'limit': '32'}

BTC_data = requests.get(BTC_data_url, params=url_params)

# Data extracted on 6/1/2018
# CryptoCompare API requires start date to be current date. As this would alter my
# data at every run, I instead saved the results from today to a static file. No
# better API is currently available for cryptocurrency(according to Reddit).

with open('BTC_data_file.txt', 'w') as outfile:
    json.dump(BTC_data.json(), outfile)


# Ethereum (2nd highest market cap)
ETH_data_url = 'https://min-api.cryptocompare.com/data/histoday'
url_params = {'fsym': 'ETH', 'tsym': 'USD', 'limit': '32'}

ETH_data = requests.get(ETH_data_url, params=url_params)

with open('ETH_data_file.txt', 'w') as outfile:
    json.dump(ETH_data.json(), outfile)


# Ripple (3rd highest market cap)
XRP_data_url = 'https://min-api.cryptocompare.com/data/histoday'
url_params = {'fsym': 'XRP', 'tsym': 'USD', 'limit': '32'}

XRP_data = requests.get(XRP_data_url, params=url_params)

with open('XRP_data_file.txt', 'w') as outfile:
    json.dump(XRP_data.json(), outfile)
'''
# DO NOT RUN THIS AGAIN.
# Needed to run only once to produce the 3 static historic price data .txt files
