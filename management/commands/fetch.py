from django.core.management.base import BaseCommand, CommandError
from syncbot.models import Settings, Project, Page, Group
from syncbot.management.libraries import mediawiki

class Command(BaseCommand):
	help = "Fetch watchlist feed from WikiMedia projects and, for pages with updates, clean revision field"

	def handle(self, *args, **options):
		for project in Project.objects.all():
			settings = Settings.objects.get(pk=1)
			token = settings.token
			
			response = mediawiki.get_watchlist_feed(
				project.domain,
				token,
				project.last_update,
			)
			
			if not response:
				raise CommandError('The MediaWiki API either did not return a response or the response was not valid')
			
			pages = mediawiki.watchlist_feed_pages(response)
			if type(pages) is list:
				for page_name in pages:
					try:
						page = Page.objects.get(
							name = page_name,
							project = project,
						)
					except Page.DoesNotExist:
						pass
					
					page.revision = 0
					page.save()
			else:
				raise CommandError('The JSON object returned from the MediaWiki API was not formatted as expected')
			
			response_timestamp = response['curtimestamp']
			project.last_update = response_timestamp
			project.save()
