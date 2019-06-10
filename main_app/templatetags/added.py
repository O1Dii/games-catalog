from django import template

from main_app.models import MustModel

register = template.Library()


@register.filter
def added(game):
    return MustModel.objects.filter(game_id=game.id, is_deleted=False).count()
