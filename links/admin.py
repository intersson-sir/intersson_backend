"""
Django Admin configuration for links app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import NegativeLink


@admin.register(NegativeLink)
class NegativeLinkAdmin(admin.ModelAdmin):
    """
    Admin interface for NegativeLink model with comprehensive filtering and actions.
    """
    
    list_display = [
        'short_url',
        'platform',
        'type',
        'status_badge',
        'priority_badge',
        'manager',
        'detected_at',
        'removed_at',
    ]
    
    list_filter = [
        'platform',
        'status',
        'priority',
        'type',
        'manager',
        'detected_at',
    ]
    
    search_fields = [
        'url',
        'manager',
        'notes',
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'detected_at',
    ]
    
    fieldsets = (
        ('Link Information', {
            'fields': ('id', 'url', 'platform', 'type')
        }),
        ('Status & Management', {
            'fields': ('status', 'priority', 'manager', 'notes')
        }),
        ('Timestamps', {
            'fields': ('detected_at', 'removed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'mark_as_removed',
        'mark_as_in_work',
        'mark_as_pending',
        'set_high_priority',
        'set_medium_priority',
        'set_low_priority',
    ]
    
    date_hierarchy = 'detected_at'
    
    def short_url(self, obj):
        """Display shortened URL with link."""
        url = obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, url)
    short_url.short_description = 'URL'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'active': '#dc3545',      # Red
            'removed': '#28a745',     # Green
            'in_work': '#ffc107',     # Yellow
            'pending': '#6c757d',     # Gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        """Display priority as colored badge."""
        colors = {
            'high': '#dc3545',        # Red
            'medium': '#ffc107',      # Yellow
            'low': '#17a2b8',         # Blue
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    # Bulk actions
    @admin.action(description='Mark selected as Removed')
    def mark_as_removed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='removed', removed_at=timezone.now())
        self.message_user(request, f'{updated} link(s) marked as removed.')
    
    @admin.action(description='Mark selected as In Work')
    def mark_as_in_work(self, request, queryset):
        updated = queryset.update(status='in_work')
        self.message_user(request, f'{updated} link(s) marked as in work.')
    
    @admin.action(description='Mark selected as Pending')
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} link(s) marked as pending.')
    
    @admin.action(description='Set priority to High')
    def set_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} link(s) set to high priority.')
    
    @admin.action(description='Set priority to Medium')
    def set_medium_priority(self, request, queryset):
        updated = queryset.update(priority='medium')
        self.message_user(request, f'{updated} link(s) set to medium priority.')
    
    @admin.action(description='Set priority to Low')
    def set_low_priority(self, request, queryset):
        updated = queryset.update(priority='low')
        self.message_user(request, f'{updated} link(s) set to low priority.')
