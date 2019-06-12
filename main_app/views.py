from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from main_app.forms import UserCreationForm
from main_app.utils import send_email
from .twitter_api import Twitter
from .tokens import account_activation_token
from .models import UserModel, Must, Game, Screenshot, Genre, Platform


class SendEmail(TemplateView):
    template_name = 'send_email.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get('active'):
            return redirect(reverse_lazy('main_app:main_page'))
        return self.render_to_response(context)

    def get_context_data(self, user_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            context['DoesNotExist'] = True
        else:
            if user.is_active:
                context['active'] = True
            else:
                send_email(self.request, user)
                context['active'] = False
        return context


# class MainPageView(LoginRequiredMixin, TemplateView):
#     template_name = 'main_page.html'
#
#     def get_context_data(self, **kwargs):
#         client = IGDB(6)
#         context = super().get_context_data(**kwargs)
#         current_page = self.request.GET.get('page', 1)
#         games = client.api_get_games_list(**{key: value for key, value in self.request.GET.items()})
#         pages_amount = client.api_get_last_pages_amount()
#         left_pages = list([str(i) for i in range(max(int(current_page) - 3, 1), int(current_page))])
#         right_pages = list([str(i) for i in range(min(int(current_page) + 1, pages_amount + 1),
#                                                   min(int(current_page) + 4, pages_amount + 1))])
#         end = int(right_pages[-1]) if right_pages else pages_amount
#         context.update({
#             'games': games,
#             'search': self.request.GET.get('search', ''),
#             'platforms': self.request.GET.get('platforms', ''),
#             'genres': self.request.GET.get('genres', ''),
#             'ur1': self.request.GET.get('ur1', '0'),
#             'ur2': self.request.GET.get('ur2', '10'),
#             'pages_amount': pages_amount,
#             'current_page': current_page,
#             'left_pages': left_pages,
#             'right_pages': right_pages,
#             'end': end
#         })
#         return context


class MainPageView(LoginRequiredMixin, ListView):
    template_name = 'main_page.html'
    model = Game
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search': self.request.GET.get('search', ''),
            'platforms': self.request.GET.get('platforms', ''),
            'genres': self.request.GET.get('genres', ''),
            'ur1': self.request.GET.get('ur1', '0'),
            'ur2': self.request.GET.get('ur2', '10'),
        })
        return context


class DetailPageView(LoginRequiredMixin, DetailView):
    template_name = 'detail_page.html'
    queryset = Game.objects.all()

    def get_context_data(self, game_id=0, **kwargs):
        context = super().get_context_data(**kwargs)
        # game = Game.objects.get(id=game_id)
        twitter = Twitter()
        tweets = list(twitter.get_tweets_via_hashtag(self.object.name))
        context['tweets'] = tweets
        # screenshots = Screenshot.objects.filter(game=game)
        # genres = Genre.objects.filter(game=game)
        # platforms = Platform.objects.filter(game=game)
        # date = 'No information'
        # if game.first_release_date:
        #     date = game.first_release_date.strftime('%Y %b %d')
        # user_rating = 'No rating'
        # if game.rating:
        #     user_rating = round(game.rating / 10, 2)
        # aggregated_rating = 'No rating'
        # if game.aggregated_rating:
        #     aggregated_rating = round(game.aggregated_rating / 10, 2)
        # context.update({
        #     'name': game.name,
        #     'version_title': game.version_title if game.version_title is not None else '',
        #     'description': game.summary if game.summary is not None else '',
        #     'release_date': date,
        #     'screenshots': [i.screenshot.url for i in screenshots],
        #     'user_ratings': user_rating,
        #     'critics_ratings': aggregated_rating,
        #     'genres': [i.genre.name for i in genres],
        #     'platforms': [i.platform.name for i in platforms],
        #     'users_reviews': game.rating_count if game.rating_count is not None else 0,
        #     'critics_reviews': game.aggregated_rating_count if game.aggregated_rating_count is not None else 0,
        #     'tweets': tweets
        # })
        return context


class RegisterPageView(FormView):
    template_name = 'login_register_page.html'
    form_class = UserCreationForm
    args_dict = {'user_id': 0}
    success_url = reverse_lazy('main_app:send_email', kwargs=args_dict)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.args_dict['user_id'] = user.id
        return super().form_valid(form)


class ActivationView(View):
    def get(self, request, uidb64, token):
        uid = 0
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse_lazy('main_app:main_page'))
        else:
            return redirect(reverse_lazy('main_app:send_email', kwargs={'user_id': uid}))


class LoginPageView(LoginView):
    template_name = 'login_register_page.html'


class LogoutPageView(LogoutView):
    pass


class UserPageView(LoginRequiredMixin, TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['age'] = round((datetime.date(datetime.now()) - self.request.user.birthday).days / 365.25)
        return context


class MustListView(LoginRequiredMixin, ListView):
    template_name = 'must_page.html'
    paginate_by = 10

    def get_queryset(self):
        # game_ids = [each.game_id for each in Must.objects.filter(user=self.request.user)]
        queryset = Must.objects.filter(user=self.request.user).all()
        # if game_ids:
        #     queryset = Game.objects.filter(id__in=game_ids)
        print(queryset[0].game)
        if len(queryset):
            return queryset
        return []


class AddRemoveMustView(View):
    def post(self, request):
        game_id = int(request.POST.get('game_id', 0))
        add = request.POST.get('add')
        force_remove = request.POST.get('force')
        if game_id:
            if add:
                must = Must.objects.get_or_create(game=Game.objects.get(id=game_id), user=request.user)
                must[0].is_deleted = False
                must[0].save()
            elif force_remove:
                must = Must.objects.get(game=Game.objects.get(id=game_id), user=request.user)
                must.delete()
            else:
                must = Must.objects.get(game=Game.objects.get(id=game_id), user=request.user)
                must.is_deleted = True
                must.save()
        return HttpResponse('')

