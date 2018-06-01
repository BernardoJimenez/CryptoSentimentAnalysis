import pandas

# Issue occurred. PyCharm kept returning the error:
# 'ImportError: DLL load failed: The specified module could not be found.'
# Solution: installing Microsoft Visual C++ Redistributable for Visual Studio 2017
date_range_index = pandas.date_range(start='4/30/2018', end='5/8/2018', normalize=True)
columns = ['BTC_high', 'BTC_low', 'BTC_median', 'BTC_median_percent_change', 'BTC_positive_sentiment',
           'ETH_high', 'ETH_low', 'ETH_median', 'ETH_median_percent_change', 'ETH_positive_sentiment',
           'XRP_high', 'XRP_low', 'XRP_median', 'XRP_median_percent_change', 'XRP_positive_sentiment']

crypto_dataframe = pandas.DataFrame(index=date_range_index, columns=columns)

print(crypto_dataframe.columns)
