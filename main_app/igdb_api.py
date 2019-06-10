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
        print(self.__headers['user-key'])
        self.__limit = limit

    def __api_get(self, additional_string: str = ''):
        print(f'{self.__api_url}{additional_string}')
        data = requests.get(f'{self.__api_url}{additional_string}', headers=self.__headers)
        j_data = data.json()
        if isinstance(j_data, list) and len(j_data):
            if isinstance(j_data[0], dict):
                if j_data[0].get('status') == 400:
                    return []
        x_count = int(data.headers.get('X-Count', 1))
        if x_count > self.__limit:
            self.__last_headers_x_count = x_count
        return j_data

    def api_get_game(self, game_id):
        category = f'games/{game_id}?'
        additional = {
            'fields': 'name,rating,version_title,aggregated_rating,'
                      'screenshots,summary,platforms,genres,first_release_date,'
                      'rating_count,aggregated_rating_count'
        }
        encoded_url = urlencode(additional)
        data = self.__api_get(f'{category}{encoded_url}')
        for i, each in enumerate(data):
            if each.get('platforms'):
                data[i]['platforms'] = self.api_get_names('platforms', each.get('platforms')).values()
            if each.get('genres'):
                data[i]['genres'] = self.api_get_names('genres', each.get('genres')).values()
            if each.get('rating'):
                data[i]['rating'] = round(each.get('rating') / 10, 2)
            if each.get('aggregated_rating'):
                data[i]['aggregated_rating'] = round(each.get('aggregated_rating') / 10, 2)
            if each.get('screenshots'):
                images = self.api_get_image(each.get('screenshots'), False)
                data[i]['screenshots'] = images.values()
        return data

    def api_get_names(self, category: str, id_list: list):
        category += '/'
        id_list = list(set(id_list))
        data = []
        if len(id_list) > 10:
            for i in range(math.floor(len(id_list) / 10)):
                data.extend(self.__api_get(category + ','.join(map(str, id_list[i * 10:(i + 1) * 10])) +
                                           '?fields=name'))
            data.extend(self.__api_get(category + ','.join(map(str,
                                                               id_list[math.floor(len(id_list) / 10) * 10:])) +
                                       '?fields=name'))
        return {each['id']: each['name'] for each in data if each.get('name')}

    def api_find(self, category: str, search: str) -> list:
        category += '/?'
        additional = {
            'search': search
        }
        encoded_url = urlencode(additional)
        data = self.__api_get(f'{category}{encoded_url}')
        if isinstance(data, list):
            return [each.get('id') for each in data]
        else:
            return []

    def __generate_filters(self, search: str = None, genres: str = None,
                           platforms: str = None, ur1: str = None, ur2: str = None, **kwargs) -> dict:
        filters = {}
        if search:
            filters['search'] = search
        if genres:
            genres = ','.join(map(str, self.api_find('genres', genres)))
            filters['filter[genres][any]'] = genres
        if platforms:
            platforms = ','.join(map(str, self.api_find('platforms', platforms)))
            filters['filter[platforms][any]'] = platforms
        if ur1 or ur2:
            ur1 = int(ur1)
            ur2 = int(ur2)
            filters['filter[rating][gt]'] = min(ur1, ur2) * 10
            filters['filter[rating][lt]'] = max(ur1, ur2) * 10
        return filters

    def api_get_last_pages_amount(self) -> int:
        """returns total amount of pages for last game list"""
        return math.ceil(self.__last_headers_x_count / self.__limit)

    def api_get_first_games(self, amount: int = 300):
        """returns the chosen amount of games"""
        category = 'games'
        fields = 'name,rating,version_title,aggregated_rating,'\
                 'screenshots,summary,platforms,genres,first_release_date,'\
                 'rating_count,aggregated_rating_count,cover'
        result = []
        if amount > 200:
            for i in range(4):
                query = f'{category}/?fields={fields}&limit=50&offset={i * 50}'
                result.extend(self.__api_get(query))
            for i in range(round((amount - 200) / 10)):
                games_list = [i * 10 + j for j in range(10)]
                print(games_list)
                query = f'{category}/{games_list}?fields={fields}'
                result.extend(self.__api_get(query))
        else:
            short_val = math.floor(amount / 50)
            for i in range(short_val):
                query = f'{category}/?fields={fields}&limit=50&offset={i * 50}'
                result.extend(self.__api_get(query))
            if amount - short_val * 50 != 0:
                query = f'{category}/?fields={fields}&limit={amount - short_val * 50}&offset={short_val * 50}'
                result.extend(self.__api_get(query))
        return result

    def api_get_games_list(self, page: str = '1', game_ids: list = None, genres: bool = False, **kwargs) -> list:
        """kwargs:
        search: str = None,
        genres: str = None,
        platforms: str = None,
        user_ratings: tuple = None"""
        category = 'games/?'
        additional = {
            'fields': 'name,cover,version_title,rating,genres',
            'limit': self.__limit,
            'offset': (int(page) - 1) * self.__limit
        }
        if game_ids:
            games = ','.join(map(str, game_ids))
            category = f'games/{games}?'
        else:
            if not kwargs.get('search'):
                additional['order'] = 'popularity:desc'
            filters = self.__generate_filters(**kwargs)
            additional.update(filters)
        encoded_url = urlencode(additional, quote_via=quote_plus)
        data = self.__api_get(f'{category}{encoded_url}')
        images_query = list(set(each.get('cover', '') for each in data if each.get('cover')))
        images = self.api_get_image(images_query, True)
        genres_list = []
        for i, each in enumerate(data):
            if each:
                if each.get('cover'):
                    data[i]['cover'] = images.get(each.get('cover'))
                if genres:
                    genres_list.append(data[i].get('genres', [0])[0])
        if genres:
            j = 0
            genre_names = self.api_get_names('genres', genres_list)
            print(genre_names)
            for i, each in enumerate(data):
                if each.get('genres'):
                    data[i]['genres'] = genre_names[each.get('genres')[0]]
                    j += 1
        return data

    def api_get_image(self, images_id: list, cover=False):
        images_id = list(set(images_id))
        result = 'covers/' if cover else 'screenshots/'
        data = []
        if len(images_id) > 10:
            for i in range(math.floor(len(images_id) / 10)):
                data.extend(self.__api_get(result + ','.join(map(str, images_id[i * 10:(i + 1) * 10])) + '?fields=url'))
            data.extend(self.__api_get(result + ','.join(map(str,
                                                             images_id[math.floor(len(images_id) / 10) * 10:])) +
                                       '?fields=url'))
        return {each.get('id'): 'https:' + each.get('url', '').replace('t_thumb', 't_cover_big' if cover
                                                                         else 't_screenshot_med') for each in data}
