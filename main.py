# Amazon Web Services (AWS) SDK for Python
import boto3
# PRAW: Python Reddit API Wrapper
import praw
# write/read JavaScript Object Notation
import json
# data structures for analysis
import pandas
# Analysis will be visualized in Tableau. As I would be using the pubic version of Tableau, if my
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


# Gathered from /r/Bitcoin
BTC_daily_threads = ['8fycit', '8g7awg', '8gg8oi', '8gp81v', '8gy393', '8h6m46', '8hea1o', '8hmcsk', '8hvicx']
# Gathered from /r/ETHtrader
ETH_daily_threads = ['8fxfii', '68ke0l', '8gf8qt', '8go8zr', '8gx487', '8h5pj3', '8hde1i', '8hleo8', '8hui5p']
# Gathered from /r/Ripple
XRP_daily_threads = ['8fxxcn', '8g6tym', '8gfs6p', '8gos16', '8gxnh7', '8h67x0', '8hdvqf', '8hlx4i', '8hv1kg']
# All from dates 4/30/2018 -> 5/8/2018

# instantiate a list to hold coin daily thread lists
coin_list_of_threads = [BTC_daily_threads, ETH_daily_threads, XRP_daily_threads]


# Function definition for scoring sentiment
def get_sentiment_scores(coin_list):
    # list to hold lists of scores for each daily thread for each coin
    list_of_score_lists = []

    for coin in coin_list:
        # list to hold scores of each daily thread for this particular coin
        coin_score_list = []

        for daily_thread in coin:
            # the url for the Reddit.com submission thread
            submission = reddit.submission(id=daily_thread)
            # remove all links in comments thread that load more comments
            submission.comments.replace_more(limit=64)

            # set initial number of sentiment scores to zero
            number_of_scores = 0
            # set initial total analysis score to zero
            total_sentiment = 0.0

            # for each comment in the submission, traversing as a breadth-first list
            # bodies of comments return as type: String
            for comment in submission.comments.list():
                # increment the number of scores/comments seen by 1
                number_of_scores += 1
                # perform sentiment analysis on the comment using Amazon Comprehend from AWS

                # ISSUE: A SINGLE COMMENT I'M PARSING IS EXCEEDING 5000 BYTES
                # SOLUTION: I MUST CHECK THE SIZE OF THE COMMENT IN BYTES BEFORE PASSING TO AWS COMPREHEND
                # WHY: AMAZON COMPREHEND RETURNS ERROR IF INPUT SIZE IS GREATER THAN 5000 BYTES
                # NOTE: I HATE REDDITORS WHO WRITE WALLS OF TEXT
                analysis = comprehend.detect_sentiment(Text=comment.body, LanguageCode='en')

                # obtain the coefficient for positiveness from the json file
                comment_score = analysis["SentimentScore"]["Positive"]
                # add the comment score to the submission's total score
                total_sentiment += comment_score
            # calculate the submission's total score by averaging all comment scores
            total_sentiment = total_sentiment/number_of_scores
            # add the total sentiment score of the daily thread to the coin's list
            coin_score_list.append(total_sentiment)
        list_of_score_lists.append(coin_score_list)
    # return the list of list of scores for each daily thread for each coin
    return list_of_score_lists


# use defined method to store scores in a list of
# lists with one list of scores for each coin
scores = get_sentiment_scores(coin_list_of_threads)

crypto_dataframe = pandas.read_csv('crypto_dataframe.csv')

crypto_dataframe['BTC_positive_sentiment'] = scores[0]
crypto_dataframe['ETH_positive_sentiment'] = scores[1]
crypto_dataframe['XRP_positive_sentiment'] = scores[2]

crypto_dataframe.to_csv('crypto_dataframe.csv')
crypto_dataframe = pandas.read_csv('crypto_dataframe.csv')
print(crypto_dataframe.to_string())
'''
# create a new file to save lists to
list_file = open('scores.txt', 'w')
# serialize to JSON (human and program readable)
json.dump(list_of_score_lists, list_file)
# close file
list_file.close()
'''
