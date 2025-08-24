from django.contrib import admin

# Register your models here.
from .models import Sector, ToolsModel, PlansModel

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'is_featured', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'name']

@admin.register(ToolsModel)
class ToolsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'tool_id', 'sector', 'is_active', 'is_featured', 'created_at']
    list_filter = ['sector', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'tool_id', 'description']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['sector']

@admin.register(PlansModel)
class PlansModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_id', 'sector', 'is_active', 'is_featured', 'created_at']
    list_filter = ['sector', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'plan_id', 'description']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['sector']
