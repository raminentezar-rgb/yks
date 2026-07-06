from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'subject', 'feedback_type', 'user_type', 'unit', 'status', 'created_at')
    list_filter = ('status', 'feedback_type', 'user_type', 'unit')
    search_fields = ('tracking_code', 'subject', 'message', 'name_surname')
    readonly_fields = ('tracking_code', 'created_at', 'updated_at')
