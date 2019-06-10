from datetime import datetime

from django.core.management import BaseCommand

from main_app.igdb_api import IGDB
from main_app.models import (GameModel, GenreModel, PlatformModel,
                             GenreGameModel, PlatformGameModel, CoverGameModel, ScreenshotGameModel,
                             CoverModel, ScreenshotModel)


class Command(BaseCommand):
    help = 'synchronizes local database with igdb database'

    def handle(self, *args, **options):
        client = IGDB(1)
        games_list = client.api_get_first_games(500)
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
                GameModel.objects.update_or_create(id=game['id'], defaults=game)

        genre_list = client.api_get_names('genres', [j for i in genres.values() for j in i])
        for genre in genre_list.items():
            GenreModel.objects.update_or_create(id=genre[0], defaults={'name': genre[1]})
        for game_genre in genres.items():
            for genre in game_genre[1]:
                GenreGameModel.objects.get_or_create(game=GameModel.objects.get(id=game_genre[0]),
                                                     genre=GenreModel.objects.get(id=genre))

        platforms_list = client.api_get_names('platforms', [j for i in platforms.values() for j in i])
        for platform in platforms_list.items():
            PlatformModel.objects.update_or_create(id=platform[0], defaults={'name': platform[1]})
        for game_platform in platforms.items():
            for platform in game_platform[1]:
                PlatformGameModel.objects.get_or_create(game=GameModel.objects.get(id=game_platform[0]),
                                                        platform=PlatformModel.objects.get(id=platform))

        covers_list = client.api_get_image(list(covers.values()), True)
        for cover in covers_list.items():
            CoverModel.objects.get_or_create(id=cover[0], url=cover[1])
        for game_cover in covers.items():
            CoverGameModel.objects.get_or_create(game=GameModel.objects.get(id=game_cover[0]),
                                                 cover=CoverModel.objects.get(id=game_cover[1]))

        screenshots_list = client.api_get_image([j for i in screenshots.values() for j in i])
        for screenshot in screenshots_list.items():
            ScreenshotModel.objects.get_or_create(id=screenshot[0], url=screenshot[1])
        for game_screenshot in screenshots.items():
            for screenshot in game_screenshot[1]:
                ScreenshotGameModel.objects.get_or_create(game=GameModel.objects.get(id=game_screenshot[0]),
                                                          screenshot=ScreenshotModel.objects.get(id=screenshot))
