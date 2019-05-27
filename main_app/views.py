from django.shortcuts import render
from django.views.generic import TemplateView

from .igdb_api import IGDB


class MainPageView(TemplateView):
    template = 'main_page.html'

    def __init__(self, **kwargs):
        super(MainPageView, self).__init__(**kwargs)
        self.client = IGDB(6)
        self.__current_page = '1'
        self.__search = ''
        self.__platforms = ''
        self.__genres = ''
        self.__user_ratings = ''

    def get_context_data(self, **kwargs):
        super(MainPageView, self).get_context_data()
        self.__current_page = self.request.GET.get('page', self.__current_page)
        print(self.request.GET)
        games = self.client.api_get_games_list(**{key: value for key, value in self.request.GET.items()})
        pages_amount = self.client.api_get_last_pages_amount()
        left_pages = list([str(i) for i in range(max(int(self.__current_page) - 3, 1), int(self.__current_page))])
        right_pages = list([str(i) for i in range(min(int(self.__current_page) + 1, pages_amount + 1),
                                                  min(int(self.__current_page) + 4, pages_amount + 1))])
        end = int(right_pages[-1]) if right_pages else pages_amount
        return {
            'games': games,
            'search': self.request.GET.get('search', ''),
            'pages_amount': pages_amount,
            'current_page': self.__current_page,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'end': end
        }
