from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def added(game):
    result = Must.objects.filter(game=game, is_deleted=False).count()
    return result
