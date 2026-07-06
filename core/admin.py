from django.contrib import admin
from .models import Announcement, SystemStat

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

@admin.register(SystemStat)
class SystemStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'count', 'new_count', 'icon')
