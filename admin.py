from django.contrib import admin

from .models import Settings, Project, Page, Group

# Register your models here.
admin.site.register(Settings)
admin.site.register(Project)

class GroupAdmin(admin.ModelAdmin):
	filter_horizontal = ['pages']
	list_display = ['page_names', 'projects']
	search_fields = ['pages__page_id', 'pages__project__domain', 'pages__revision', 'pages__name']

class PageAdmin(admin.ModelAdmin):
	readonly_fields = ['name']
	list_display = ['name', 'project']
	search_fields = ['name', 'project__domain', 'page_id', 'revision']
	list_filter = ['project']

admin.site.register(Group, GroupAdmin)
admin.site.register(Page, PageAdmin)
