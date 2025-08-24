from django.urls import path
from .views import get_sector_names, get_enhanced_prompt

urlpatterns = [
    path('sectors/', get_sector_names, name='get_sector_names'),
    path('enhance-prompt/', get_enhanced_prompt, name='get_enhanced_prompt'),
]