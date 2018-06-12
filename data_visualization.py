# data structures for analysis
import pandas as pd
# functions for data visualization
import seaborn as sns
# plotting functions
import matplotlib.pyplot as plt


# read in dataframe from .csv file
crypto_dataframe = pd.read_csv('crypto_dataframe.csv')
# rename column with dates to 'Date'
crypto_dataframe.rename(columns={'Unnamed: 0.1': 'Date'}, inplace=True)
# drop column with index numbers
crypto_dataframe.drop(labels='Unnamed: 0', axis=1, inplace=True)
# set 'Date' column as the index
crypto_dataframe.set_index('Date', inplace=True)
# reset index keeping 'Dates' column
crypto_dataframe.reset_index(inplace=True)

# create Bitcoin dataframe using relevant data and standardizing column names
BTC_df = pd.concat([crypto_dataframe['BTC_median_percent_change'][1:].reset_index(drop=True),
                    crypto_dataframe['BTC_positive_sentiment'][:8].reset_index(drop=True)], axis=1, ignore_index=True)\
    .rename(columns={0: 'Median Percent Change', 1: 'Positive Sentiment Score the Day Before'}) \
    .join(pd.Series(['Bitcoin'] * 8, name='Cryptocurreny'))  # add column indicating cryptocurrency name
# Ethereum
ETH_df = pd.concat([crypto_dataframe['ETH_median_percent_change'][1:].reset_index(drop=True),
                    crypto_dataframe['ETH_positive_sentiment'][:8].reset_index(drop=True)], axis=1, ignore_index=True)\
    .rename(columns={0: 'Median Percent Change', 1: 'Positive Sentiment Score the Day Before'}) \
    .join(pd.Series(['Ethereum'] * 8, name='Cryptocurreny'))
# Ripple
XRP_df = pd.concat([crypto_dataframe['XRP_median_percent_change'][1:].reset_index(drop=True),
                    crypto_dataframe['XRP_positive_sentiment'][:8].reset_index(drop=True)], axis=1, ignore_index=True)\
    .rename(columns={0: 'Median Percent Change', 1: 'Positive Sentiment Score the Day Before'}) \
    .join(pd.Series(['Ripple'] * 8, name='Cryptocurreny'))

# final dataframe contains column for sentiment, column for median change, and column for crypto name
processed_df = pd.concat([BTC_df, ETH_df, XRP_df], ignore_index=True)


# create dictionary to hold color for each coin
pal = dict(Bitcoin="pink", Ethereum="teal", Ripple="gold")
# use FacetGrid to plot multiple plots on one grid
g = sns.FacetGrid(processed_df, hue='Cryptocurreny', palette=pal, size=5);
g.map(plt.scatter, "Positive Sentiment Score the Day Before", "Median Percent Change",
      s=50, alpha=.7, linewidth=.5, edgecolor="white")
g.map(sns.regplot, "Positive Sentiment Score the Day Before", "Median Percent Change", ci=None, robust=1)
# add title
g.fig.suptitle('Relationship between Sentiment\n and Median Price Change')
# create linear regression line of best fit using all data from crypto
g_all = sns.regplot(processed_df['Positive Sentiment Score the Day Before'], processed_df['Median Percent Change'],
                    scatter=False, fit_reg=True, ci=None, label='Total line of best fit',
                    line_kws={'color': 'black'})
# specify what data to use for legend creation
handles_, labels_ = plt.gca().get_legend_handles_labels()
g_all.legend(handles_[0:4], labels_[0:4], numpoints=1,
             title='Cryptocurrencies', fontsize='x-small', fancybox=True, bbox_to_anchor=(1.18, 0.3))
# save figure to image file
g.savefig('seaborn_linreg_visualization.png')
