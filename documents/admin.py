from django.contrib import admin
from .models import DocumentCategory, Document

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'icon')
    search_fields = ('name', 'code')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category', 'unit', 'revision_number', 'download_count', 'is_active')
    list_filter = ('category', 'unit', 'is_active')
    search_fields = ('code', 'title', 'unit')
    readonly_fields = ('download_count', 'created_at')
