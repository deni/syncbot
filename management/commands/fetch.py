from django.core.management.base import BaseCommand, CommandError
from syncbot.management.libraries import syncbot

class Command(BaseCommand):
	help = "Fetch watchlist feed from WikiMedia projects and, for pages with updates, clean revision field"

	def handle(self, *args, **options):
		syncbot.fetch()

