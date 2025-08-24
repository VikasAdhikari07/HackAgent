from django.shortcuts import render
from portia import Portia, PlanUUID
from .config import default_config
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Sector
from .sectorTools.marketingTool import register_marketing_tools
from .sectorTools.researchTools import register_research_tools
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


@api_view(['POST'])
def get_plan(request):
    """
    API endpoint to fetch a plan based on the request parameters.
    
    Returns:
        Response: JSON response containing the plan data
        
    Example response:
    """
    try:
        # Get the request data
        data = request.data
        
        # Get the sector name from the request data
        sector_name = data.get('sector')
        prompt = data.get('prompt')
        print(sector_name)
        print(prompt)
        # Get the plan based on the sector name
        if sector_name == 'marketing':
            tools = register_marketing_tools()
        elif sector_name == 'research':
            tools = register_research_tools()
            print("****@@@@@@@@@@@@@*****", tools.get_tools())
        else:
            tools = None
        plan = Portia(config=default_config, tools=tools).plan(prompt)
        return Response({
            'success': True,
            'data': plan.model_dump()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        raise e
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch plan'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def run_plan(request):
    """
    API endpoint to run a plan based on the request parameters.
    """
    try:
        data = request.data
        plan_id = data.get('plan_id')
        sector_name = data.get('sector')
        if sector_name == 'marketing':
            tools = register_marketing_tools()
        elif sector_name == 'research':
            tools = register_research_tools()
        else:
            tools = None
        
        portia = Portia(config=default_config, tools=tools)
        
        run = portia.run_plan(plan=PlanUUID.from_string(plan_id))
        return Response({
            'success': True,
            'data': run.model_dump()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to run plan'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)