from django.contrib import admin
from .models import DiscussProject

@admin.register(DiscussProject)
class DiscussProjectAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'contact_method', 'created_at')
    search_fields = ('full_name', 'email', 'project_description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
