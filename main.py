# Amazon Web Services (AWS) SDK for Python
import boto3
# PRAW: Python Reddit API Wrapper
import praw
# requests library used to make HTTP calls
import requests
# configure the OS date and time
import win32api
# write/read JavaScript Object Notation
import json


# The state of this project thus far is a proof of concept, using the technologies as intended.
# The completed state will incorporate the Reddit API, CoinMarketCap API, and AWS to determine
# how sentiment affects the price change in a coin on a per day basis... Analysis will be
# visualized in Tableau. As I would be using the pubic version of Tableau, if my
# visuals are not able to be exported/downloaded, I'll switch to using the Python package Seaborn instead.

# attach comprehend service to variable, making sure to use hardcode region wth that service
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
'''
text = "Bananas are fruit."
# print entire json file
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
'''

# instantiate an instance of a read-only Reddit class
# comments separated by the user
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='N68ksfBmQXwJWQ', client_secret="YGqrNjKYWAq7rluaXSm_21O5ZJw")

# the url for the Reddit.com submission thread
submission = reddit.submission(id='8gvvuz')
# remove all links in comments thread that load more comments
submission.comments.replace_more(limit=None)

# set initial number of sentiment scores to zero
number_of_scores = 0
# set initial total analysis score to zero
total_sentiment = 0.0
'''
# for each comment in the submission, traversing as a breadth-first list
# bodies of comments return as type: String
for comment in submission.comments.list():
    # increment the number of scores/comments seen by 1
    number_of_scores += 1
    # perform sentiment analysis on the comment using Amazon Comprehend from AWS
    analysis = comprehend.detect_sentiment(Text=comment.body, LanguageCode='en')
    # obtain the coefficient for positiveness from the json file
    comment_score = analysis["SentimentScore"]["Positive"]
    # add the comment score to the submission's total score
    total_sentiment += comment_score
# calculate the submission's total score by averaging all comment scores
total_sentiment = total_sentiment/number_of_scores
# print the total sentiment score
print(total_sentiment)  # 0.25074256019619073 as of 05/22/18
'''

# Using CryptoCompare site's API: https://min-api.cryptocompare.com
# use 'Historical Daily OHLCV' API Historical Data section
BTC_data_url = 'https://min-api.cryptocompare.com/data/histoday'
url_params = {'fsym': 'BTC', 'tsym': 'USD', 'limit': '7'}

# In order to change system time, disable Admin Approval Mode in:
# Local Security Policy > Local Policies > Security Options
win32api.SetSystemTime(2018, 5, 1, 8, 0, 0, 0, 0)
# to reset: Set the Time and Date > Internet Time > Change Settings > Update Now
# The purpose of setting the System time to May 7th is so i could extract a precise
# range of dates to use with the CryptoCompare API. The API has no option for start
# date, and thus forces the user to start from the current date. However, I now
# see the API was never using my System date and instead used their own server's (duh)
# As such, my plan now is to extract the dates I want and save the JSON to a static text
# file to parse values from so my data does not change on each run. To do this, I'll use
# the CryptoCompare API in a separate Python file and save the results.

BTC_data = requests.get(BTC_data_url, params=url_params)
print(BTC_data.json())
