from django.urls import path, register_converter
from .views import (MainPageView, DetailPageView,
                    RegisterPageView, LoginPageView, LogoutPageView,
                    UserPageView, ActivationView, SendEmail)
from .utils import TokenConverter

app_name = 'main_app'

register_converter(TokenConverter, 'token')

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('detail/<int:game_id>', DetailPageView.as_view(), name='detail_page'),
    path('registration', RegisterPageView.as_view(), name='register_page'),
    path('logout', LogoutPageView.as_view(), name='logout'),
    path('login', LoginPageView.as_view(), name='login_page'),
    path('user', UserPageView.as_view(), name='user_page'),
    path('activate/<slug:uidb64>/<token:token>', ActivationView.as_view(), name='activate'),
    path('send_email/<int:user_id>', SendEmail.as_view(), name='send_email')
]
