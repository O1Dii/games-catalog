from django.core.management import BaseCommand

from main_app.tasks import sync_igdb_task


class Command(BaseCommand):
    help = 'synchronizes local database with igdb database'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        sync_igdb_task.delay(options['amount'])
