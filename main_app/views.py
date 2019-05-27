from django.views.generic import TemplateView

from .igdb_api import IGDB


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        client = IGDB(6)
        context = super(MainPageView, self).get_context_data(**kwargs)
        current_page = self.request.GET.get('page', 1)
        games = client.api_get_games_list(**{key: value for key, value in self.request.GET.items()})
        pages_amount = client.api_get_last_pages_amount()
        left_pages = list([str(i) for i in range(max(int(current_page) - 3, 1), int(current_page))])
        right_pages = list([str(i) for i in range(min(int(current_page) + 1, pages_amount + 1),
                                                  min(int(current_page) + 4, pages_amount + 1))])
        end = int(right_pages[-1]) if right_pages else pages_amount
        context['games'] = games
        context['search'] = self.request.GET.get('search', '')
        context['pages_amount'] = pages_amount
        context['current_page'] = current_page
        context['left_pages'] = left_pages
        context['right_pages'] = right_pages
        context['end'] = end
        return context
