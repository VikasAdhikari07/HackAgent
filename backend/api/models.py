from django.db import models

# Create your models here.
class Sector(models.Model):
    """
    Model to represent different sectors/work areas that the platform covers.
    This will help categorize and organize the various business domains
    and industries that the marketing agent can work with.
    """
    
    # Basic sector information
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Name of the sector (e.g., Technology, Healthcare, Finance)"
    )
    
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        help_text="URL-friendly version of the sector name"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this sector encompasses"
    )
    
    # Categorization
    category = models.CharField(
        max_length=50,
        choices=[
            ('industry', 'Industry'),
            ('service', 'Service'),
            ('technology', 'Technology'),
            ('nonprofit', 'Non-Profit'),
            ('government', 'Government'),
            ('education', 'Education'),
            ('other', 'Other'),
        ],
        default='industry',
        help_text="High-level category for this sector"
    )
    
    # Status and visibility
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this sector is currently active and available"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this sector prominently"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Ordering and display
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order for displaying sectors (lower numbers appear first)"
    )
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically generate slug from name
        if slug is not provided.
        """
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ToolsModel(models.Model):
    """
    Model to represent the tools that the marketing agent can use.
    This will help the agent perform its tasks and achieve its goals.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the tool (e.g., Google Search, Wikipedia, etc.)"
    )
    tool_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="ID of the tool (e.g., google-search, wikipedia, etc.)"
    )
    sectors = models.ManyToManyField(Sector, help_text="Sectors that can use this tool")
    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this tool does"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this tool is currently active and available"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this tool prominently"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'
    
    
    
class PlansModel(models.Model):
    """
    Model to represent the plans that the marketing agent can use.
    This will help the agent perform its tasks and achieve its goals.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the plan (e.g., Basic, Pro, Enterprise)"
    )
    plan_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="ID of the plan (e.g., basic, pro, enterprise)"
    )
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, help_text="Sector of the plan")

    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this plan does"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this plan is currently active and available"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this plan prominently"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Plan'
    