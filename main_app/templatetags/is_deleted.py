from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def is_deleted(game):
    return Must.objects.get(game_id=game.id).is_deleted
