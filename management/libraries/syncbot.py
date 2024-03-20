from syncbot.models import Settings, Project, Page, Group
from syncbot.management.libraries import mediawiki
import logging

logger = logging.getLogger(__name__)


def fetch():
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
					logger.warning("The API returned a watchlist page that was not found locally")
				
				page.revision = 0
				page.save()
				logger.info(f"The page {page_name} on {project} was marked as updated")
		else:
			raise CommandError('The JSON object returned from the MediaWiki API was not formatted as expected')
		
		response_timestamp = response['curtimestamp']
		project.last_update = response_timestamp
		project.save()


def synchronize():
	groups = Group.objects.filter(pages__revision = 0)
	for group in groups:
		pages_updated = group.pages.filter(revision = 0)
		
		if len(pages_updated) == 1:
			source = pages_updated.get()
			targets = group.pages.exclude(pk = source.pk)
			
			logger.info(f"The page {source.name} on {source.project} has new changes; attempting to copy the page content to other pages in the group ...")
			
			settings = Settings.objects.get(pk=1)
			token = settings.token
					
			source_response = mediawiki.page_read(
				source.project.domain,
				token,
				source.name,
			)
			
			source_latest = source_response['query']['pages'][0]['revisions'][0]
			source_latest_id = source_latest['revid']
			source_latest_minor = source_latest['minor']
			source_latest_content = source_latest['slots']['main']['content']
			
			source_domain = source.project.domain
			source_language_code = source_domain.partition('.')[0]
			
			success = 1
			for target in targets:
				summary = 'Synchronize to {}:{}'.format(
					source_language_code,
					source_latest_id,
				)
				
				result = mediawiki.page_edit(
					target.project.domain,
					token,
					target.name,
					target.revision,
					source_latest_content,
					summary,
					source_latest_minor,
				)
				
				if result['edit']['result'] != 'Success':
					success = 0
					logger.info(f"{target.project}, {target.name}: Failed; the API did not return success")
				
				if 'newrevid' in result['edit']:
					target_latest_id = result['edit']['newrevid']
					target.revision = int(target_latest_id)
					target.save()
					
					logger.info(f"{target.project}, {target.name}: Success")
				else:
					success = 0
					logger.info(f"{target.project}, {target.name}: Failed; the API did not return a new revision ID")
			
			source.revision = source_latest_id
			source.save()
			if success:
				logger.info("The page group was successfully synchronized")
			else:
				logger.info("There was/were error(s) in the synchronization of the page group")
		else:
			# disable group
			pass

