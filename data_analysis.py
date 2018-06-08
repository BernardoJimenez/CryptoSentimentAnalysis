# data structures for analysis
import pandas
# Machine Learning algorithms
import sklearn.linear_model


# read in dataframe from .csv file
crypto_dataframe = pandas.read_csv('crypto_dataframe.csv')
# rename column with dates to 'Date'
crypto_dataframe.rename(columns={'Unnamed: 0.1': 'Date'}, inplace=True)
# drop column with index numbers
crypto_dataframe.drop(labels='Unnamed: 0', axis=1, inplace=True)
# set 'Date' column as the index
crypto_dataframe.set_index('Date', inplace=True)

# create Bitcoin dataframe using only columns pertaining to Bitcoin
BTC_df = crypto_dataframe[crypto_dataframe.columns[crypto_dataframe.columns.str.startswith('BTC')]]
# create Ethereum dataframe
ETH_df = crypto_dataframe[crypto_dataframe.columns[crypto_dataframe.columns.str.startswith('ETH')]]
# create Ripple dataframe
XRP_df = crypto_dataframe[crypto_dataframe.columns[crypto_dataframe.columns.str.startswith('XRP')]]


# Create file to write linear regression results to
analysis_results_file = open("analysis_results.txt", "w")

# Bitcoin
# set features for linear regression to be sentiment scores, with last value before the last day
BTC_X = pandas.DataFrame(BTC_df['BTC_positive_sentiment']).iloc[:8]
# set dependant target variable to be median percent change, with first value starting at the second day
# Reasoning: I'm searching for the affect in median price change due to the sentiment the DAY BEFORE
BTC_y = pandas.DataFrame(BTC_df['BTC_median_percent_change']).iloc[1:]
# fit the linear regression model with the data
BTC_linreg = sklearn.linear_model.LinearRegression().fit(BTC_X, BTC_y['BTC_median_percent_change'])
# R-squared value: how good our model fits the data / explains this% of the variance in our dependent variable
analysis_results_file.write("The R-squared score for the Bitcoin linear regression model is {}\n"
                            .format(BTC_linreg.score(BTC_X, BTC_y['BTC_median_percent_change'])))
# Intercept: theoretical value for change in price when positive sentiment is zero
analysis_results_file.write("The y-intercept for the Bitcoin model is {}\n".format(BTC_linreg.intercept_))
# coefficient 'b' in the linear regression model y = mx + b
analysis_results_file.write("The coefficient for the Bitcoin predictor is {}\n\n".format(BTC_linreg.coef_))

# Ethereum
ETH_X = pandas.DataFrame(ETH_df['ETH_positive_sentiment']).iloc[:8]
ETH_y = pandas.DataFrame(ETH_df['ETH_median_percent_change']).iloc[1:]
ETH_linreg = sklearn.linear_model.LinearRegression().fit(ETH_X, ETH_y['ETH_median_percent_change'])
analysis_results_file.write("The R-squared score for the Ethereum linear regression model is {}\n"
                            .format(ETH_linreg.score(ETH_X, ETH_y['ETH_median_percent_change'])))
analysis_results_file.write("The y-intercept for the Ethereum model is {}\n".format(ETH_linreg.intercept_))
analysis_results_file.write("The coefficient for the Ethereum predictor is {}\n\n".format(ETH_linreg.coef_))


# Ripple
XRP_X = pandas.DataFrame(XRP_df['XRP_positive_sentiment']).iloc[:8]
XRP_y = pandas.DataFrame(XRP_df['XRP_median_percent_change']).iloc[1:]
XRP_linreg = sklearn.linear_model.LinearRegression().fit(XRP_X, XRP_y['XRP_median_percent_change'])
analysis_results_file.write("The R-squared score for the Ripple linear regression model is {}\n"
                            .format(XRP_linreg.score(XRP_X, XRP_y['XRP_median_percent_change'])))
analysis_results_file.write("The y-intercept for the Ripple model is {}\n".format(XRP_linreg.intercept_))
analysis_results_file.write("The coefficient for the Ripple predictor is {}\n\n".format(XRP_linreg.coef_))

# All top three coins used for linear regression
crypto_X = pandas.DataFrame(pandas.concat([BTC_df['BTC_positive_sentiment'][:8], ETH_df['ETH_positive_sentiment'][:8],
                            XRP_df['XRP_positive_sentiment'][:8]], ignore_index=True))
crypto_y = pandas.concat([BTC_df['BTC_median_percent_change'][1:], ETH_df['ETH_median_percent_change'][1:],
                          XRP_df['XRP_median_percent_change'][1:]], ignore_index=True)
crypto_linreg = sklearn.linear_model.LinearRegression().fit(crypto_X, crypto_y)
analysis_results_file.write("The R-squared score for the 'all top 3 coins' linear regression model is {}\n"
                            .format(crypto_linreg.score(crypto_X, crypto_y)))
analysis_results_file.write("The y-intercept for the top-3-coins model is {}\n".format(crypto_linreg.intercept_))
analysis_results_file.write("The coefficient for the top-3 predictor is {}".format(crypto_linreg.coef_))

# close file
analysis_results_file.close()
