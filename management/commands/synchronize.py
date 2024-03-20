from django.core.management.base import BaseCommand, CommandError
from syncbot.management.libraries import syncbot

class Command(BaseCommand):
	help = "Queries local database and uses the information to synchronize page groups"

	def handle(self, *args, **options):
		syncbot.synchronize()

