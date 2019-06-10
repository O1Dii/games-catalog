from django import template

from main_app.models import CoverGameModel

register = template.Library()


@register.filter
def cover(game):
    try:
        cover = CoverGameModel.objects.get(game=game)
    except CoverGameModel.DoesNotExist:
        print('no cover for', game.name)
        return ''
    return cover.cover.url
