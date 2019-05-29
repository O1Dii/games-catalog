from django.urls import path
from .views import MainPageView, DetailPageView, RegisterPageView

app_name = 'main_app'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('detail/<int:game_id>', DetailPageView.as_view(), name='detail_page'),
    path('registration', RegisterPageView.as_view(), name='register_page')
]
