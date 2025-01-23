from django.db import models
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

# Create your models here.

class Settings(models.Model):
	token = models.TextField()
	
	class Meta:
		verbose_name_plural = "Settings"


class Project(models.Model):
	domain = models.CharField(max_length=200)
	last_update = models.CharField(max_length=200)
	
	def __str__(self):
		return self.domain


class Page(models.Model):
	name = models.CharField(max_length=200)
	page_id = models.PositiveBigIntegerField()
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	revision = models.PositiveBigIntegerField()
	
	def __str__(self):
		template = '{}; {}'
		string = template.format(
			self.project,
			self.name,
		)
		
		return(string)


class Group(models.Model):
	pages = models.ManyToManyField(Page)
	current = models.BooleanField()

	def page_names(self):
		page_names = []
		for page in self.pages.all():
			if not page.name in page_names:
				page_names.append(page.name)

		return( format_html_join(
				mark_safe('<br>'),
				'{}',
				( (line,) for line in page_names )
			)
		)


	def projects(self):
		project_domains = []
		for page in self.pages.all():
			if not page.project.domain in project_domains:
				project_domains.append(page.project.domain)
		
		return(
			format_html_join(
				mark_safe('<br>'),
				'{}',
				( (line,) for line in project_domains )
			)
		)
