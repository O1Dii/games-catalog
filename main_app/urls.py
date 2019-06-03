from django.urls import path, re_path
from .views import MainPageView, DetailPageView, \
    RegisterPageView, LoginPageView, LogoutPageView, \
    UserPageView, ActivationView, SendEmail

app_name = 'main_app'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('detail/<int:game_id>', DetailPageView.as_view(), name='detail_page'),
    path('registration', RegisterPageView.as_view(), name='register_page'),
    path('logout', LogoutPageView.as_view(), name='logout'),
    path('login', LoginPageView.as_view(), name='login_page'),
    path('user', UserPageView.as_view(), name='user_page'),
    re_path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
            ActivationView.as_view(), name='activate'),
    path('send_email/<int:user_id>', SendEmail.as_view(), name='send_email')
]
