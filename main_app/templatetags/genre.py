from django import template

from main_app.models import GenreGameModel

register = template.Library()


@register.filter
def genre(game):
    genres = GenreGameModel.objects.filter(game=game)
    if genres:
        return genres[0].genre.name
    return ''
