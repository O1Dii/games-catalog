from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def is_deleted(game):
    try:
        return Must.objects.get(game=game).is_deleted
    except Must.DoesNotExist:
        return True
