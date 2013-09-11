#!/usr/bin/env python

from social_collector import twitter, settings
import pika
import sys

# initialize rabbitmq connection:
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.rabbitmq['host']))
channel = rabbitmq_connection.channel()
#define a direct rabbitmq exchange:
channel.exchange_declare(exchange='tweets', exchange_type='direct')

# initialize Twitter connection:
twitter = twitter.Twitter(**settings.oauth)

for tweet_str in twitter.stream(sys.argv[1]):
    try:
        #publish tweet:
        print "publishing tweet..."
        channel.basic_publish (exchange='tweets', routing_key='', body=tweet_str)
    except Exception as e:
        print tweet_str
        print e
        continue

#close rabbitmq connection:
rabbitmq_connection.close()







 
