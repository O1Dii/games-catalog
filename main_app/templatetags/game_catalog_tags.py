from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def added(game):
    return Must.objects.filter(game=game, is_deleted=False).count()


@register.filter
def divide(value, arg):
    try:
        return round(int(value) / int(arg), 2)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def is_deleted(game):
    try:
        return Must.objects.get(game=game).is_deleted
    except Must.DoesNotExist:
        return True