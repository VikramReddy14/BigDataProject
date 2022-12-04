import tweepy


bearer_token = "AAAAAAAAAAAAAAAAAAAAAAkajwEAAAAACoklzU5Y6z%2BQfSDuqJbWpOmOvPU%3D115RjOCiJ75DIP9vSbHSFxoC65K6xheIdgB0uxJJ8IxNvTmlPE"

client = tweepy.Client(bearer_token)

response = client.search_recent_tweets("Covid")

print(response.meta)

tweets = response.data

# Each Tweet object has default ID and text fields
for tweet in tweets:
    print(tweet.id)
    print(tweet.text)