from django import template

from main_app.models import Must

register = template.Library()


@register.filter
def added(game):
    return Must.objects.filter(game_id=game.id, is_deleted=False).count()
