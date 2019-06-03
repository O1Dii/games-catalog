from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, FormView

from main_app.forms import UserCreationForm
from main_app.utils import send_email
from .igdb_api import IGDB
from .twitter_api import Twitter
from .tokens import account_activation_token
from .models import UserModel


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


class MainPageView(LoginRequiredMixin, TemplateView):
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


class DetailPageView(LoginRequiredMixin, TemplateView):
    template_name = 'detail_page.html'

    def get_context_data(self, game_id, **kwargs):
        context = super().get_context_data(**kwargs)
        client = IGDB(6)
        game = client.api_get_game(game_id)[0]
        twitter = Twitter()
        tweets = list(twitter.get_tweets_via_hashtag(game.get('name')))
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
            'critics_reviews': game.get('aggregated_rating_count', '0'),
            'tweets': tweets
        })
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


class UserPageView(TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['age'] = round((datetime.date(datetime.now()) - self.request.user.birthday).days / 365.25)
        return context
