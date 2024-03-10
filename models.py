from django.db import models

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
