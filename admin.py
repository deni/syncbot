from django.contrib import admin

from .models import Settings, Project, Page, Group

# Register your models here.
admin.site.register(Settings)
admin.site.register(Project)
admin.site.register(Page)

class GroupAdmin(admin.ModelAdmin):
	filter_horizontal = ['pages']

admin.site.register(Group, GroupAdmin)


