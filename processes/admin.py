from django.contrib import admin
from .models import ProcessCard, JobDefinition

@admin.register(ProcessCard)
class ProcessCardAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner', 'created_at')
    search_fields = ('code', 'name', 'owner', 'purpose')

@admin.register(JobDefinition)
class JobDefinitionAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'updated_at')
    search_fields = ('code', 'title', 'department')
    list_filter = ('department',)
