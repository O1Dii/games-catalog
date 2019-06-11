from django import template

from main_app.models import MustModel

register = template.Library()


@register.filter
def is_deleted(game):
    return MustModel.objects.get(game_id=game.id).is_deleted
