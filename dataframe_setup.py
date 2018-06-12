# write/read JavaScript Object Notation
import json
# data structures for analysis
import pandas

# Issue occurred. PyCharm kept returning the error:
# 'ImportError: DLL load failed: The specified module could not be found.'
# Solution: installing Microsoft Visual C++ Redistributable for Visual Studio 2017
date_range_index = pandas.date_range(start='4/30/2018', end='5/8/2018', normalize=True)
columns = ['BTC_high', 'BTC_low', 'BTC_median', 'BTC_median_percent_change', 'BTC_positive_sentiment',
           'ETH_high', 'ETH_low', 'ETH_median', 'ETH_median_percent_change', 'ETH_positive_sentiment',
           'XRP_high', 'XRP_low', 'XRP_median', 'XRP_median_percent_change', 'XRP_positive_sentiment']

crypto_dataframe = pandas.DataFrame(index=date_range_index, columns=columns)
# Replace all NaN values with 0
crypto_dataframe.fillna(0, inplace=True)


# load BTC data from text file into a JSON object
with open('BTC_data_file.txt', 'r') as coin_obj:
    BTC_data = json.load(coin_obj)

# instantiate lists to hold BTC values from JSON object
BTC_highs = []
BTC_lows = []
BTC_medians = []

# iterate through the JSON object
for day in BTC_data['Data'][:9]:
    # collect the highs and lows for the first nine days in the object
    BTC_highs.append(day['high'])
    BTC_lows.append(day['low'])
    # calculate the median value for that day
    BTC_medians.append((day['high'] + day['low'])/2)

# instantiate a list to hold the percent changes in median value
BTC_medians_change = []
# start from index 1 since no percent change in day we start from
index = 1
# iterate through the medians list
while index < len(BTC_medians):
    # calculate the percent increase
    value = ((BTC_medians[index] - BTC_medians[index - 1]) / BTC_medians[index - 1]) * 100
    # add value to medians change list
    BTC_medians_change.append(value)
    # increment the index
    index += 1
# append 0 to the beginning of the list, since logically the change on first day is 0
BTC_medians_change.insert(0, 0)

# set each list created as the corresponding dataFrame column
crypto_dataframe['BTC_high'] = BTC_highs
crypto_dataframe['BTC_low'] = BTC_lows
crypto_dataframe['BTC_median'] = BTC_medians
crypto_dataframe['BTC_median_percent_change'] = BTC_medians_change


# Ethereum
with open('ETH_data_file.txt', 'r') as coin_obj:
    ETH_data = json.load(coin_obj)

ETH_highs = []
ETH_lows = []
ETH_medians = []

for day in ETH_data['Data'][:9]:
    ETH_highs.append(day['high'])
    ETH_lows.append(day['low'])
    ETH_medians.append((day['high'] + day['low'])/2)

ETH_medians_change = []
index = 1
while index < len(ETH_medians):
    value = ((ETH_medians[index] - ETH_medians[index - 1]) / ETH_medians[index - 1]) * 100
    ETH_medians_change.append(value)
    index += 1
ETH_medians_change.insert(0, 0)

crypto_dataframe['ETH_high'] = ETH_highs
crypto_dataframe['ETH_low'] = ETH_lows
crypto_dataframe['ETH_median'] = ETH_medians
crypto_dataframe['ETH_median_percent_change'] = ETH_medians_change


# Ripple
with open('XRP_data_file.txt', 'r') as coin_obj:
    XRP_data = json.load(coin_obj)

XRP_highs = []
XRP_lows = []
XRP_medians = []

for day in XRP_data['Data'][:9]:
    XRP_highs.append(day['high'])
    XRP_lows.append(day['low'])
    XRP_medians.append((day['high'] + day['low'])/2)

XRP_medians_change = []
index = 1
while index < len(XRP_medians):
    value = ((XRP_medians[index] - XRP_medians[index - 1]) / XRP_medians[index - 1]) * 100
    XRP_medians_change.append(value)
    index += 1
XRP_medians_change.insert(0, 0)

crypto_dataframe['XRP_high'] = XRP_highs
crypto_dataframe['XRP_low'] = XRP_lows
crypto_dataframe['XRP_median'] = XRP_medians
crypto_dataframe['XRP_median_percent_change'] = XRP_medians_change


# Save current dataframe to csv file
crypto_dataframe.to_csv('crypto_dataframe.csv')
# All that is missing is the sentiment columns
print(crypto_dataframe.to_string())
