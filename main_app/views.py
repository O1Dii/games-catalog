from datetime import datetime
from urllib.parse import urlencode

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from main_app.forms import UserCreationForm
from main_app.utils import send_email, search_in_queryset, auth_token_check
from .twitter_api import Twitter
from .models import UserModel, Must, Game, Genre, Platform


class GamesFilteredQuerysetMixin:
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        platforms = self.request.GET.get('platforms', '')
        genres = self.request.GET.get('genres', '')
        try:
            ur1 = int(self.request.GET.get('ur1', 0))
            ur2 = int(self.request.GET.get('ur2', 10))
        except ValueError:
            ur1 = 0
            ur2 = 10
        if ur1 > ur2:
            ur1, ur2 = ur2, ur1
        platforms = search_in_queryset(Platform.objects.all(), platforms)
        genres = search_in_queryset(Genre.objects.all(), genres)
        if ur2 - ur1 == 10:
            queryset = Game.objects.filter(platforms__in=platforms, genres__in=genres).distinct()
        else:
            queryset = Game.objects.filter(platforms__in=platforms, genres__in=genres,
                                           rating__range=(ur1 * 10, ur2 * 10 + 1)).distinct()
        queryset = search_in_queryset(queryset, search)
        return queryset


class SendEmail(TemplateView):
    template_name = 'send_email.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get('active'):
            return redirect(reverse_lazy('main_app:main_page'))
        return self.render_to_response(context)

    def get_context_data(self, user_id=0, **kwargs):
        context = super().get_context_data(**kwargs)
        if user_id == 0:
            context['DoesNotExist'] = True
            return context
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


class MainPageView(GamesFilteredQuerysetMixin, LoginRequiredMixin, ListView):
    template_name = 'main_page.html'
    model = Game
    paginate_by = 6
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = {
            'search': self.request.GET.get('search', ''),
            'platforms': self.request.GET.get('platforms', ''),
            'genres': self.request.GET.get('genres', ''),
            'ur1': self.request.GET.get('ur1', '0'),
            'ur2': self.request.GET.get('ur2', '10'),
        }
        context['query'] = urlencode(query)
        context.update(query)
        return context


class DetailPageView(LoginRequiredMixin, DetailView):
    template_name = 'detail_page.html'
    model = Game
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        twitter = Twitter()
        tweets = list(twitter.get_tweets_via_hashtag(self.object.name))
        context['tweets'] = tweets
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
        user = auth_token_check(uidb64, token)
        if user:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse_lazy('main_app:main_page'))
        else:
            return redirect(reverse_lazy('main_app:send_email'))


class LoginPageView(LoginView):
    template_name = 'login_register_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['log_in'] = True
        return context


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
    context_object_name = 'musts'

    def get_queryset(self):
        temp = Must.objects.filter(user=self.request.user)
        return temp


class AddRemoveMustView(View):
    def post(self, request):
        game_id = int(request.POST['game_id'])
        add = request.POST.get('add')
        if add:
            must = Must.objects.get_or_create(game=Game.objects.get(id=game_id), user=request.user)
            must[0].is_deleted = False
            must[0].save()
        else:
            Must.objects.get(game=Game.objects.get(id=game_id), user=request.user).delete()
        return HttpResponse('')
