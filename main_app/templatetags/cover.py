from django import template

from main_app.models import Cover

register = template.Library()


@register.filter
def cover(game):
    try:
        cover = Cover.objects.get(game=game)
    except Cover.DoesNotExist:
        print('no cover for', game.name)
        return ''
    return cover.cover.url
