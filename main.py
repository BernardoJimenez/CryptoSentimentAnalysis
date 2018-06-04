# Amazon Web Services (AWS) SDK for Python
import boto3
# PRAW: Python Reddit API Wrapper
import praw
# write/read JavaScript Object Notation
import json
# data structures for analysis
import pandas as pd


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

BTC_data = json.load('BTC_data_file.txt')["Data"]
