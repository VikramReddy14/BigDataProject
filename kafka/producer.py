import time
import json
import tweepy
from json import dumps
from kafka import KafkaProducer

#Twitter API Authentication

with open('config.json') as json_file:
    data = json.load(json_file)
bearer_token=data["bearer_token"]
client = tweepy.Client(bearer_token)


response=client.search_recent_tweets(query="iphone OR Musk",max_results=100,tweet_fields=['created_at','lang'],expansions=['author_id'])
users={u['id']: u for u in response.includes['users']}

counts=client.get_recent_tweets_count("NewYork",granularity='day')
counts_retweets=client.get_recent_tweets_count('covid -is:retweet',granularity='day')

#Extracting User_ID of the Following User
user_details=client.get_users(usernames=['twitterdev'])

#Getting User Tweets of the following User
response1=client.get_liked_tweets(id=data['user_id'],tweet_fields=['lang'])

tweets = response.data
new_topic_tweets = response1.data
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda K:json.dumps(K).encode('utf-8'))
producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],key_serializer=lambda m:dumps(m).encode('utf-8'),value_serializer=lambda K:dumps(K).encode('utf-8'))

topic_name = 'Twitter-Kafka'
topic_name1="User-Liked"
topic_name_count="Count"
topic_name_covid_retweet="Covid-Retweet"

#Function for sending Covid Retweet counts to consumer
def get_covid_retweet_counts():
    for count in counts_retweets.data:
        producer.send(topic_name_covid_retweet,json.dumps(count))

#Function for sending Newyork tweet counts to consumer
def get_tweet_counts():
    for count in counts.data:
        print(json.dumps(count))
        producer.send(topic_name_count,json.dumps(count))

#get_tweet_counts()

def get_twitter_data1():

        for tweet in tweets:
            if(tweet.lang=='en'):
                user=users[tweet.author_id]
                print(user.username)
                #my_bytes = tweet.encode('utf-8')
                #print(my_bytes)
                producer1.send(topic_name,key=tweet.id,value=tweet.text)
                #producer.send(topic_name,tweet.id)
                print(tweet.id)
                print(tweet.lang)

#get_twitter_data1()

def get_twitter_data2():
    for tweet in new_topic_tweets:
        if(tweet.lang=='en'):
            producer1.send(topic_name1,key=tweet.id,value=tweet.text)
            print(tweet.id)

#get_twitter_data2()