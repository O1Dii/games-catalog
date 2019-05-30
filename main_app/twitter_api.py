from datetime import datetime
from urllib.parse import quote

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

    def __parse_tweets(self, tweets):
        result = []
        for tweet in tweets:
            result.append({
                'date': datetime.strptime(tweet['created_at'],
                                          '%a %b %d %X %z %Y').strftime('%d.%m.%Y %H:%M'),
                'text': tweet['text'],
                'author': tweet['user']['name']
            })
        return result

    def get_tweets_via_hashtag(self, search: str):
        encoded_search = quote('#' + search)
        my_url = f'{self.__search_url}?q={encoded_search}'
        response = requests.get(my_url, auth=self.__oauth)
        return self.__parse_tweets(response.json()['statuses']) if response.status_code == 200 else []
