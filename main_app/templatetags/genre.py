from django import template

from main_app.models import Genre

register = template.Library()


@register.filter
def genre(game):
    genres = Genre.objects.filter(game=game)
    if genres:
        return genres[0].genre.name
    return ''
