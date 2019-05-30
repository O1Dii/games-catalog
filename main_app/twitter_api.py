from urllib.parse import urlencode

import requests
from requests_oauthlib import OAuth1
from django.conf import settings


class Twitter:
    def __init__(self):
        self.__search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.__oauth = OAuth1(settings.CONSUMER_TOKEN,
                              settings.CONSUMER_TOKEN_SECRET,
                              resource_owner_key=settings.ACCESS_TOKEN,
                              resource_owner_secret=settings.ACCESS_TOKEN_SECRET)

    def get_tweets_via_hashtag(self, search: str):
        encoded_search = urlencode('#' + search)
        my_url = f'{self.__search_url}?{encoded_search}'
        print(my_url)
        print(settings.CONSUMER_TOKEN, settings.CONSUMER_TOKEN_SECRET,
              settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        r = requests.get(my_url, auth=self.__oauth).json()
        return r
