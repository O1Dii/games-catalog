import requests


class IGDB:
    api_key = 'ca03e6492746de9c40fb685c0b1fe80b'
    api_url = 'https://api-v3.igdb.com/'
    headers = {
        'user-key': api_key,
        'Accept': 'application/json'
    }

    def api_get(self, additional_string: ''):
        result = self.api_url + additional_string
        print(result)
        data = requests.get(result, headers=self.headers).json()
        print(data)
        for each in data:
            screens = each.get('screenshots')
            cover = each.get('cover')
            if screens is not None:
                for i in screens:
                    self.api_get_image(i)
            if cover is not None:
                self.api_get_image(cover, True)

    def api_get_game(self, first_argument: str = '', search: str = None, fields: str = None, filters: str = None):
        additional = 'games/' + first_argument + '?'
        if search is not None:
            additional += ('search=' + search.replace(' ', '%20') + '&')
        if fields is not None:
            additional += ('fields=' + fields.replace(' ', '') + '&')
        if filters is not None:
            additional += ('filters=' + filters)
        self.api_get(additional)

    def api_get_image(self, id, cover=False):
        result = self.api_url + ('covers/' if cover else 'screenshots/')
        data = requests.get(result + str(id) + '?fields=url', headers=self.headers).json()
        print('https:' + data[0].get('url').replace('t_thumb', 't_logo_med' if cover else 't_screenshot_med'))


temp = IGDB()
temp.api_get_game(search=input('Введите название игры'),
                  fields='screenshots,cover')

# rating, version_title, aggregated_rating, screenshots, summary, cover, platforms, genres

# {'id': 45553, 'first_release_date': 681004800}, {'id': 37337}

