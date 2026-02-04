from django.contrib import admin
from .models import Industry, Template

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    def has_add_permission(self, request):
        # Prevent adding if 10 exist
        if Industry.objects.count() >= 10:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry', 'created_at')
    list_filter = ('industry',)
    search_fields = ('title', 'industry__name')

    def has_add_permission(self, request):
        return True
        
    # Validation in model clean() handles the count check
