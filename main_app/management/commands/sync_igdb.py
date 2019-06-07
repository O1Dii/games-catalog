from django.core.management import BaseCommand

from main_app.igdb_api import IGDB
from main_app.models import (GameModel, GenreModel, PlatformModel, ImageModel,
                             GenreGameModel, PlatformGameModel, CoverGameModel, ScreenshotGameModel)


class Command(BaseCommand):
    help = 'synchronizes local database with igdb database'

    def handle(self, *args, **options):
        client = IGDB(1)
        client.api_get_games_list()
        GameModel.objects.get_or_create()
