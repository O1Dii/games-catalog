from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='main_page.html'), name='main_page'),
    path('detail', TemplateView.as_view(template_name='detail_page.html'), name='detail_page'),
]
