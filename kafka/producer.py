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
tweets = response.data
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda K:json.dumps(K).encode('utf-8'))
producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],key_serializer=lambda m:dumps(m).encode('utf-8'),value_serializer=lambda K:dumps(K).encode('utf-8'))

topic_name = 'Twitter-Kafka'


def get_twitter_data1():

        for tweet in tweets:
            if(tweet.lang=='en'):
                
                #my_bytes = tweet.encode('utf-8')
                #print(my_bytes)
                producer1.send(topic_name,key=tweet.id,value=tweet.text)
                #producer.send(topic_name,tweet.id)
                print(tweet.id)
                print(tweet.lang)
#get_twitter_data1()