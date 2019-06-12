from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def is_deleted(game):
    try:
        obj = Must.objects.get(game=game)
        deleted = obj.is_deleted
        return deleted
    except Must.DoesNotExist:
        return True
