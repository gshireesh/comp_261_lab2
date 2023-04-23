import json
import os
import tweepy
from dotenv import dotenv_values

config = dotenv_values(".env")

consumer_key = config["API_KEY"]
consumer_secret = config["API_KEY_SECRET"]
access_token = config["ACCESS_TOKEN"]
access_token_secret = config["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

api = tweepy.API(auth)

tweets = api.search_tweets("ukraine", tweet_mode="extended")
if __name__ == '__main__':
    data = []
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        data.append(tweet)

    with open("twitter_data.json", "w") as outfile:
        json.dump(data, outfile)
