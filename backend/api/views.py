from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Sector

@api_view(['GET'])
def get_sector_names(request):
    """
    API endpoint to fetch all sector names.
    
    Returns:
        Response: JSON response containing a list of sector names
        
    Example response:
    {
        "success": true,
        "data": [
            {
                "id": 1,
                "name": "Technology",
                "slug": "technology",
                "category": "industry"
            },
            {
                "id": 2,
                "name": "Healthcare",
                "slug": "healthcare", 
                "category": "industry"
            }
        ],
        "count": 2
    }
    """
    try:
        # Fetch only active sectors, ordered by their order field and name
        sectors = Sector.objects.filter(is_active=True).values(
            'id', 'name', 'slug', 'category'
        )
        
        return Response({
            'success': True,
            'data': list(sectors),
            'count': len(sectors)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch sector names'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


