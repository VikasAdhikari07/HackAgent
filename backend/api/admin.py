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
    # Fixed: Use 'sectors' instead of 'sector' since it's a ManyToManyField
    list_display = ['name', 'tool_id', 'get_sectors', 'is_active', 'is_featured', 'created_at']
    list_filter = ['sectors', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'tool_id', 'description']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['sectors']  # Better UI for ManyToMany instead of raw_id_fields
    
    def get_sectors(self, obj):
        """Display sectors in list view"""
        return ", ".join([sector.name for sector in obj.sectors.all()])
    get_sectors.short_description = 'Sectors'

@admin.register(PlansModel)
class PlansModelAdmin(admin.ModelAdmin):
    # This one is correct since PlansModel has 'sector' (ForeignKey)
    list_display = ['name', 'plan_id', 'sector', 'is_active', 'is_featured', 'created_at']
    list_filter = ['sector', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'plan_id', 'description']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['sector']
