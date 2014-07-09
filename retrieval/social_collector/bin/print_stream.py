#!/usr/bin/env python

from social_collector import twitter, settings
import argparse
import pika
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print a realtime twitter stream')
    parser.add_argument('--keywords', dest="keywords", help='Keywords to use for filtering Twitter stream', nargs='+')
    args = parser.parse_args()

    # initialize Twitter connection:
    twitter = twitter.Twitter(**settings.twitter)

    for tweet_str in twitter.stream(args.keywords):
        print "*"*50
        print tweet_str
        print "*"*50







 
