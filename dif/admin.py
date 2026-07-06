from django.contrib import admin
from .models import DifRecord

@admin.register(DifRecord)
class DifRecordAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'unit', 'finding_type', 'responsible_person', 'target_date', 'status')
    list_filter = ('status', 'finding_type', 'unit')
    search_fields = ('code', 'title', 'root_cause', 'action_plan', 'responsible_person')
    readonly_fields = ('created_at',)
