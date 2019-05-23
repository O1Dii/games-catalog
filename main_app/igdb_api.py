import requests
from math import ceil
from itechart_project.settings import IGDB_API_KEY


class IGDB:
    __api_key = IGDB_API_KEY
    __api_url = 'https://api-v3.igdb.com/'
    __headers = {
        'user-key': __api_key,
        'Accept': 'application/json'
    }

    def __init__(self):
        self.__last_headers_x_count = 1

    def __api_get(self, additional_string: str = ''):
        data = requests.get(self.__api_url + additional_string, headers=self.__headers)
        x_count = int(data.headers.get('X-Count'))
        if x_count > 1:
            self.__last_headers_x_count = x_count
        return data.json()

    def api_get_game(self, game_id):
        data = self.__api_get(f'games/{game_id}?fields=rating,version_title,aggregated_rating,'
                              f' screenshots,summary,cover,platforms,genres')
        print(data)
        return data

    def __generate_filters(self, search: str = None, genres: str = None,
                           platforms: str = None, user_ratings: tuple = None) -> str:
        result = []
        if search is not None:
            result.append(f'&search={search.replace(" ", "%20")}&')
        if any((genres, platforms, user_ratings)):
            result.append('filter')
        if genres is not None:
            result.append(f'[genres][eq]={genres},')
        if platforms is not None:
            result.append(f'[platforms][eq]={platforms},')
        if user_ratings is not None:
            try:
                result.append(f'[rating][gt]={user_ratings[0]},[rating][lt]={user_ratings[1]},')
            except IndexError as e:
                print(e)
        if len(result) != 0:
            return ''.join(result)[:-1]
        else:
            return ''

    def api_get_last_pages_amount(self) -> int:
        """returns total amount of pages for last game list"""
        return ceil(self.__last_headers_x_count / 6)

    def api_get_games_list(self, page: int = 0, **kwargs) -> list:
        """kwargs:
        search: str = None,
        genres: str = None,
        platforms: str = None,
        user_ratings: tuple = None"""
        additional = f'games/?fields=name,cover,version_title&limit=6&offset={page * 6}'
        if kwargs.get('search') is None:
            additional += '&order=popularity:desc'
        filters = self.__generate_filters(**kwargs)
        data = self.__api_get(additional + filters)
        for i in range(len(data)):
            if data[i].get('cover') is not None:
                data[i]['cover'] = self.api_get_image(data[i].get('cover'), True)
        print(data)
        return data

    def api_get_image(self, image_id: int, cover=False) -> str:
        result = 'covers/' if cover else 'screenshots/'
        data = self.__api_get(result + str(image_id) + '?fields=url')
        return 'https:' + data[0].get('url').replace('t_thumb', 't_logo_med' if cover else 't_screenshot_med')
