import tweepy
from config import *

#Authentication variables from config.py:
#twitter_key
#twitter_secret
#twitter_token
#twitter_token_secret

def twitter_auth():
    auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    twitter = tweepy.API(auth)
    return twitter

def getTweets(twitter, hashtag, n_tweets):
    return tweepy.Cursor(twitter.search, q=hashtag).items(n_tweets)