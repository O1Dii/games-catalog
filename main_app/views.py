from datetime import datetime

from django.views.generic import TemplateView

from .igdb_api import IGDB


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        client = IGDB(6)
        context = super().get_context_data(**kwargs)
        current_page = self.request.GET.get('page', 1)
        games = client.api_get_games_list(**{key: value for key, value in self.request.GET.items()})
        pages_amount = client.api_get_last_pages_amount()
        left_pages = list([str(i) for i in range(max(int(current_page) - 3, 1), int(current_page))])
        right_pages = list([str(i) for i in range(min(int(current_page) + 1, pages_amount + 1),
                                                  min(int(current_page) + 4, pages_amount + 1))])
        end = int(right_pages[-1]) if right_pages else pages_amount
        context.update({
            'games': games,
            'search': self.request.GET.get('search', ''),
            'platforms': self.request.GET.get('platforms', ''),
            'genres': self.request.GET.get('genres', ''),
            'ur1': self.request.GET.get('ur1', '0'),
            'ur2': self.request.GET.get('ur2', '10'),
            'pages_amount': pages_amount,
            'current_page': current_page,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'end': end
        })
        return context


class DetailPageView(TemplateView):
    template_name = 'detail_page.html'

    def get_context_data(self, game_id, **kwargs):
        context = super().get_context_data(**kwargs)
        client = IGDB(6)
        game = client.api_get_game(game_id)[0]
        print(game)
        context.update({
            'name': game.get('name', ''),
            'version_title': game.get('version_title', ''),
            'description': game.get('summary', ''),
            'release_date': datetime.utcfromtimestamp(game.get('first_release_date')).strftime('%Y %b %d'),
            'screenshots': game.get('screenshots'),
            'user_ratings': game.get('rating', '0'),
            'critics_ratings': game.get('aggregated_rating', '0'),
            'genres': game.get('genres'),
            'platforms': game.get('platforms'),
            'users_reviews': game.get('rating_count', '0'),
            'critics_reviews': game.get('aggregated_rating_count', '0')
        })
        return context

