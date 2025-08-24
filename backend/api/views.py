from unicodedata import category
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Sector
from google import genai 
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)
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
def get_enhanced_prompt(request):
    """
    API endpoint to get enhanced prompt.
    
    Returns:
        Response: JSON response containing the enhanced prompt
        
    Example response:
    {
        "success": true,
        "data": "Enhanced prompt text"
    }
    """

        # name = "marketing"
        # category = "SaaS product launch"
        # user_query = "I need to launch a product marketing campaign for a new SaaS tool. Please help me:"

    

    print(request.data,"request.data")
    category = request.data.get('category')
    name = request.data.get('name')
    user_query = request.data.get('user_query')
    try:
        contents = f"""
        Based on the sector name '{name}' and category '{category}', and the following user query:

        '{user_query}'

        Generate the 10 most important and sequential action steps required. 
        provide max upto 50 words and less than that. 
        Return the response in **valid JSON format** with this structure:

        
        "steps": [
            "Step 1 description",
            "Step 2 description",
            "Step 10 description"
        ]
       
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
        )
        print(response.text)
        return Response({
            'success': True,
            'data': response.text,
            'message': 'Enhanced prompt retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to get enhanced prompt'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    