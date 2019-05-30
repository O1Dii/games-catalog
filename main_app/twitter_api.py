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

    def get_tweets_via_hashtag(self, search: str):
        encoded_search = quote('#' + search)
        my_url = f'{self.__search_url}?q={encoded_search}'
        r = requests.get(my_url, auth=self.__oauth).json().get('statuses')
        if r:
            for each in r:
                result = {
                    'date': datetime.strptime(each.get('created_at'),
                                              '%a %b %d %X %z %Y').strftime('%d.%m.%Y %H:%M'),
                    'text': each.get('text')
                }
                user = each.get('user', {}).get('name')
                if user:
                    result['author'] = user
                yield result
        return []
