import math
from urllib.parse import urlencode, quote_plus

import requests

from django.conf import settings


class IGDB:
    def __init__(self, limit):
        self.__last_headers_x_count = 1
        self.__api_url = 'https://api-v3.igdb.com/'
        self.__headers = {
            'user-key': settings.IGDB_API_KEY,
            'Accept': 'application/json'
        }
        self.__limit = limit

    def __api_get(self, additional_string: str = ''):
        print(f'{self.__api_url}{additional_string}')
        data = requests.get(f'{self.__api_url}{additional_string}', headers=self.__headers)
        x_count = int(data.headers.get('X-Count', 1))
        if x_count > 1:
            self.__last_headers_x_count = x_count
        return data.json()

    def api_get_game(self, game_id):
        category = f'games/{game_id}?'
        additional = {
            'fields': 'rating,version_title,aggregated_rating,'
                      'screenshots,summary,cover,platforms,genres'
        }
        encoded_url = urlencode(additional)
        data = self.__api_get(f'{category}{encoded_url}')
        return data

    def __generate_filters(self, search: str = None, genres: str = None,
                           platforms: str = None, user_ratings: tuple = None) -> dict:
        result = {}
        filters = []
        if search:
            result['search'] = search
        if genres:
            filters.append(f'[genres][eq]={genres}')
        if platforms:
            filters.append(f'[platforms][eq]={platforms}')
        if user_ratings:
            filters.append('[rating]')
            if user_ratings[0]:
                filters[-1] += f'[gt]={user_ratings[0] * 10}'
            if user_ratings[0] and user_ratings[1]:
                filters[-1] += ','
            if user_ratings[1]:
                filters[-1] += f'[lt]={user_ratings[1] * 10}'
        if filters:
            result[''] = f'filter{",".join(filters)}'
        return result

    def api_get_last_pages_amount(self) -> int:
        """returns total amount of pages for last game list"""
        return math.ceil(self.__last_headers_x_count / self.__limit)

    def api_get_games_list(self, page: int = 0, **kwargs) -> list:
        """kwargs:
        search: str = None,
        genres: str = None,
        platforms: str = None,
        user_ratings: tuple = None"""
        category = 'games/?'
        additional = {
            'fields': 'name,cover,version_title,rating',
            'limit': self.__limit,
            'offset': page * self.__limit}
        if kwargs.get('search') is None:
            additional['order'] = 'popularity:desc'
        filters = self.__generate_filters(**kwargs)
        additional.update(filters)
        encoded_url = urlencode(additional, quote_via=quote_plus)
        data = self.__api_get(f'{category}{encoded_url}')
        for i, each in enumerate(data):
            if each:
                if each.get('cover'):
                    data[i]['cover'] = self.api_get_image(each.get('cover'), True)
        return data

    def api_get_image(self, image_id: int, cover=False) -> str:
        result = 'covers/' if cover else 'screenshots/'
        data = self.__api_get(result + str(image_id) + '?fields=url')
        return 'https:' + data[0].get('url').replace('t_thumb', 't_logo_med' if cover
                                                     else 't_screenshot_med')
