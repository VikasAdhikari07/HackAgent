from django.urls import path
from .views import get_sector_names, get_enhanced_prompt
from .views import get_sector_names, get_plan, run_plan

urlpatterns = [
    path('sectors/', get_sector_names, name='get_sector_names'),
    path('enhance-prompt/', get_enhanced_prompt, name='get_enhanced_prompt'),
    path('plan/', get_plan, name='get_plan'),
    path('run_plan/', run_plan, name='run_plan'),
]