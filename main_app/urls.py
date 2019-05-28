from django.urls import path
from .views import MainPageView, DetailPageView

app_name = 'main_app'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('detail/<int:game_id>', DetailPageView.as_view(), name='detail_page')
]
