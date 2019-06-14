from datetime import datetime

from django.core.management import BaseCommand

from main_app.igdb_api import IGDB
from main_app.models import (Game, Genre, Platform, Cover, Screenshot)


class Command(BaseCommand):
    help = 'synchronizes local database with igdb database'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        client = IGDB(1)
        games_list = client.api_get_first_games(options['amount'])
        covers = {}
        screenshots = {}
        platforms = {}
        genres = {}
        for game in games_list:
            if isinstance(game, str):
                continue
            if game.get('genres'):
                genres[game['id']] = game['genres']
                del game['genres']
            if game.get('platforms'):
                platforms[game['id']] = game['platforms']
                del game['platforms']
            if game.get('screenshots'):
                screenshots[game['id']] = game['screenshots']
                del game['screenshots']
            if game.get('cover'):
                covers[game['id']] = game['cover']
                del game['cover']
            if game.get('first_release_date'):
                game['first_release_date'] = datetime.utcfromtimestamp(game['first_release_date']).strftime('%Y-%m-%d')
            if game.get('status') not in [500, 404, 401, 403]:
                Game.objects.update_or_create(id=game['id'], defaults=game)

        genre_list = client.api_get_names('genres', [j for i in genres.values() for j in i])
        for genre in genre_list.items():
            Genre.objects.update_or_create(id=genre[0], defaults={'name': genre[1]})
        for game_genre in genres.items():
            for genre in game_genre[1]:
                temp_genre = Genre.objects.get(id=genre)
                temp_genre.games.add(Game.objects.get(id=game_genre[0]))

        platforms_list = client.api_get_names('platforms', [j for i in platforms.values() for j in i])
        for platform in platforms_list.items():
            Platform.objects.update_or_create(id=platform[0], defaults={'name': platform[1]})
        for game_platform in platforms.items():
            for platform in game_platform[1]:
                temp_platform = Platform.objects.get(id=platform)
                temp_platform.games.add(Game.objects.get(id=game_platform[0]))

        covers_list = client.api_get_image(list(covers.values()), True)
        # for cover in covers_list.items():
        #     Cover.objects.get_or_create(id=cover[0], url=cover[1])
        for game_cover in covers.items():
            Cover.objects.get_or_create(game=Game.objects.get(id=game_cover[0]),
                                        url=covers_list[game_cover[1]])

        screenshots_list = client.api_get_image([j for i in screenshots.values() for j in i])
        # for screenshot in screenshots_list.items():
        #     Screenshot.objects.get_or_create(id=screenshot[0], url=screenshot[1])
        for game_screenshot in screenshots.items():
            for screenshot in game_screenshot[1]:
                Screenshot.objects.get_or_create(game=Game.objects.get(id=game_screenshot[0]),
                                                 url=screenshots_list[screenshot])
