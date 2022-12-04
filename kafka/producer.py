import tweepy
import json
import tweepy

#Twitter API Authentication

with open('config.json') as json_file:
    data = json.load(json_file)
bearer_token=data["bearer_token"]
client = tweepy.Client(bearer_token)

response = client.search_recent_tweets("Covid")

print(response.meta)

tweets = response.data

# Each Tweet object has default ID and text fields
for tweet in tweets:
    print(tweet.id)
    print(tweet.text)