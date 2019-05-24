from django.shortcuts import render
from django.views import View
from .igdb_api import IGDB


class MainPageView(View):
    template = 'main_page.html'

    def __init__(self):
        super(MainPageView, self).__init__()
        self.client = IGDB(6)
        self.__current_page = '1'

    def get(self, request):
        context = {
            'games': self.client.api_get_games_list(),
            'pages_amount': self.client.api_get_last_pages_amount(),
            'current_page': self.__current_page,
            'left_pages': None,
            'right_pages': '23',
            'end': 3
        }
        return render(request, self.template, context)

    def post(self, request):
        self.__current_page = request.POST.get('page', self.__current_page)
        games = self.client.api_get_games_list(**{key: value for key, value in request.POST.items()})
        pages_amount = self.client.api_get_last_pages_amount()
        left_pages = list([str(i) for i in range(max(int(self.__current_page) - 3, 1), int(self.__current_page))])
        right_pages = list([str(i) for i in range(min(int(self.__current_page) + 1, pages_amount),
                                                  min(int(self.__current_page) + 4, pages_amount))])
        context = {
            'games': games,
            'pages_amount': pages_amount,
            'current_page': self.__current_page,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'end': int(right_pages[-1])
        }
        return render(request, self.template, context)
