from django.urls import path
from .views import MainPageView, DetailPageView, RegisterPageView, LoginPageView, LogoutPageView

app_name = 'main_app'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('detail/<int:game_id>', DetailPageView.as_view(), name='detail_page'),
    path('registration', RegisterPageView.as_view(), name='register_page'),
    path('logout', LogoutPageView.as_view(), name='logout'),
    path('login', LoginPageView.as_view(), name='login_page')
]
