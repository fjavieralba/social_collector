from requests_oauthlib import OAuth1
import datetime
import requests

class Twitter(object):

    def __init__(self, access_token=None, access_token_secret=None, 
                consumer_key=None, consumer_secret=None, proxies=None):
        self.oauth = OAuth1(consumer_key,
                            client_secret=consumer_secret,
                            resource_owner_key=access_token,
                            resource_owner_secret=access_token_secret)
        self.proxies = proxies


    def stream(self, keywords):
        """
            connects to twitter stream API and yields received tweets
        """
        stream = requests.post('https://stream.twitter.com/1/statuses/filter.json',
                                data={'track': keywords}, auth=self.oauth, stream=True,
                                proxies=self.proxies)
        return stream.iter_lines()

    def search(self, **kwargs):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        response = requests.get(url, params=kwargs, auth=self.oauth, proxies=self.proxies)
        return response.content

    def user_timeline(self, **kwargs):
        """
            Thin wrapper over user_timeline API's method
            more info: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
        """
        # for some obscure reason, using requests payload will result in oauth authentication error
        # because of that we use this more rudimentary process:
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
        response = requests.get(url, params=kwargs, auth=self.oauth, proxies=self.proxies)
        return response.content

class TweetAnalyzer(object):
    """
        Class to analyze tweets content and return only interesting parts
    """

    def __init__(self):
        pass

    def extract_hashtags(self, tweet):
        try:
            hashtags = tweet['entities']['hashtags']
            return [hashtag['text'] for hashtag in hashtags]
        except:
            return []


    def extract_mentioned_users(self, tweet):
        try:
            user_mentions = tweet['entities']['user_mentions']
            return [user['screen_name'] for user in user_mentions]
        except:
            return []

    def extract_urls(self, tweet):
        """
            return a list of tuples (url, expanded_url)
        """
        try:
            urls = tweet['entities']['urls']
            return [(url['url'], url['expanded_url']) for url in urls]
        except:
            return []

    def extract_timestamp(self, tweet):
        try:
            tweet_date = tweet['created_at']
            return datetime.datetime.strptime(tweet_date, "%a %b %d %H:%M:%S +0000 %Y")
        except:
            return None