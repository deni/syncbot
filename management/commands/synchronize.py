from django.core.management.base import BaseCommand, CommandError
from syncbot.models import Settings, Project, Page, Group
from syncbot.management.libraries import mediawiki

class Command(BaseCommand):
	help = "Queries local database and uses the information to synchronize page groups"

	def handle(self, *args, **options):
		groups = Group.objects.filter(pages__revision = 0)
		for group in groups:
			pages_updated = group.pages.filter(revision = 0)
			
			if len(pages_updated) == 1:
				source = pages_updated.get()
				targets = group.pages.exclude(pk = source.pk)
				
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
						# disable page
						pass
					
					if 'newrevid' in result['edit']:
						target_latest_id = result['edit']['newrevid']
						target.revision = int(target_latest_id)
						target.save()
					else:
						# disable page
						pass
				
				source.revision = source_latest_id
				source.save()
			else:
				# disable group
				pass
