from django.contrib import admin
from .models import Review

@admin.action(description='Approve selected reviews')
def approve_reviews(modeladmin, request, queryset):
    queryset.update(is_approved=True)

@admin.action(description='Reject (hide) selected reviews')
def reject_reviews(modeladmin, request, queryset):
    queryset.update(is_approved=False)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('first_name', 'last_name', 'company_name', 'review_text')
    actions = [approve_reviews, reject_reviews]
    list_editable = ('is_approved',)
