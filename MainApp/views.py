from django.views.generic import TemplateView
from .models import GameImage


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = GameImage.objects.all()
        return context
