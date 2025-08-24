from django.urls import path
from .views import get_sector_names

urlpatterns = [
    path('sectors/', get_sector_names, name='get_sector_names'),
]