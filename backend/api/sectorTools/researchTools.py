from portia import PortiaToolRegistry, ToolRegistry, open_source_tool_registry, config, tool
import cohere
from ..config import default_config
from typing import Dict
from dotenv import load_dotenv
import os
from portia import tool
import requests
from typing import List, Dict
from kaggle.api.kaggle_api_extended import KaggleApi
from portia import ToolRegistry
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

@tool
def save_tool(content: str, filename: str = "output.txt") -> str:
    """Save the given content to a file. and return"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Content saved to {filename}"

@tool
def enhance_writing_cohere(text: str, tone: str = "neutral") -> Dict[str, str]:
    """
    Enhance and improve writing quality using Cohere's language model API.
    
    This tool takes input text and applies grammar corrections, clarity improvements,
    and tone adjustments to produce more polished and professional writing.

    Args:
        text (str): The input text that needs to be enhanced and improved
        tone (str): The desired writing tone for the output. Options include:
                   - "neutral": Balanced, objective tone
                   - "formal": Professional, academic style
                   - "casual": Conversational, friendly tone  
                   - "persuasive": Compelling, convincing style

    Returns:
        Dict[str, str]: A dictionary containing:
            - enhanced (str): The improved version of the input text with better
                            grammar, clarity, and the specified tone applied
    
    Example:
        result = enhance_writing_cohere("this text need improve", "formal")
        # Returns: {"enhanced": "This text requires improvement."}
    """
    prompt = f"Improve the following text for grammar, clarity, and tone. Make it {tone}:\n\n{text}"

    response = co.generate(
        model="command-light",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )

    enhanced_text = response.generations[0].text.strip()

    return {
        "enhanced": enhanced_text
    }

@tool
def search_huggingface_datasets(keyword: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search for datasets on Hugging Face platform using a keyword query.
    
    This tool connects to the Hugging Face API to find relevant datasets based on your search term.
    It's particularly useful for finding machine learning datasets, text corpora, image collections,
    and other research data hosted on the Hugging Face platform.

    Args:
        keyword (str): The search term to find relevant datasets. Can be:
                      - Topic names (e.g., "sentiment analysis", "medical imaging")
                      - Data types (e.g., "text", "audio", "vision")
                      - Domain areas (e.g., "finance", "healthcare", "nlp")
                      - Specific dataset names or partial names
        max_results (int): Maximum number of dataset results to return (default: 5)
                          Helps control response size and processing time

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a dataset with:
            - "name" (str): The unique dataset identifier/ID on Hugging Face
            - "link" (str): Direct URL to access the dataset on Hugging Face platform
            - "source" (str): Always "HuggingFace" to identify the data source
            - "description" (str): Brief description of the dataset content and purpose,
                                 or "No description" if not available

    Use Cases:
        - Finding training data for machine learning models
        - Discovering benchmark datasets for research
        - Locating domain-specific datasets for analysis
        - Exploring available data in a particular field

    Example Usage:
        # Search for sentiment analysis datasets
        datasets = search_huggingface_datasets("sentiment analysis", 3)
        
        # Search for medical datasets  
        medical_data = search_huggingface_datasets("medical", 10)
    """
    url = f"https://huggingface.co/api/datasets?search={keyword}"
    response = requests.get(url)

    if response.status_code != 200:
        return [{"message": f"Failed to fetch Hugging Face datasets (status {response.status_code})"}]

    data = response.json()
    if not data:
        return [{"message": f"No datasets found for keyword: {keyword}"}]

    results = []
    for d in data[:max_results]:
        results.append({
            "name": d.get("id", "Unknown"),
            "link": f"https://huggingface.co/datasets/{d.get('id', '')}",
            "source": "HuggingFace",
            "description": d.get("cardData", {}).get("description", "No description")
        })

    return results


@tool
def search_kaggle_datasets(keyword: str) -> str:
    """
    Search Kaggle datasets by keyword and return formatted results with titles and direct links.
    
    This function searches the Kaggle platform for datasets matching the specified keyword
    and returns a string containing the top matching results with titles and direct URLs.
    
    Args:
        keyword (str): Search term to find relevant datasets on Kaggle.
                      Can include:
                      - Subject areas (e.g., "machine learning", "finance", "healthcare")
                      - Data types (e.g., "time series", "image", "text")
                      - Specific topics or domain names
    
    Returns:
        str: A formatted string where each line contains:
             - Dataset title
             - Direct URL to the dataset on Kaggle platform
             Format: "Dataset Title | https://www.kaggle.com/datasets/dataset-ref"
             Returns "No datasets found for keyword: {keyword}" if no results found.
    
    Use Cases:
        - Finding publicly available datasets for research projects
        - Discovering competition datasets and benchmarks
        - Locating real-world data for analysis and modeling
        - Exploring domain-specific datasets with community ratings
    
    Example Usage:
        # Search for financial datasets
        financial_data = search_kaggle_datasets("stock market")
        
        # Search for image datasets
        image_data = search_kaggle_datasets("computer vision")
    """
    
    api = KaggleApi()
    api.authenticate()
    datasets = api.dataset_list(search=keyword)
    if not datasets:
        return f"No datasets found for keyword: {keyword}"

    results = []
    for d in datasets:
        results.append(f"{d.title} | https://www.kaggle.com/datasets/{d.ref}")

    return "\n".join(results)

def register_research_tools():
    current_research_registry = ToolRegistry([
        save_tool(),
        enhance_writing_cohere(),
        search_huggingface_datasets(),
        search_kaggle_datasets()
    ])
    # Get Portia cloud tools
    print("🔍 Loading Portia cloud tools...")
    portia_cloud_registry = PortiaToolRegistry(config=default_config)
    print(f"✅ Loaded {len(portia_cloud_registry)} cloud tools")
    
    # Extract specific local tools from open source registry
    local_tools = []
    desired_local_tools = [
        "search_tool",
        "crawl_tool", 
        "extract_tool",
        "image_understanding_tool"
    ]
        
    for tool in open_source_tool_registry.get_tools():
        if tool.id in desired_local_tools:
            local_tools.append(tool)
            print(f"✅ Added local tool: {tool.id}")
    
    # Extract specific Portia cloud tools
    cloud_tools = []
    desired_cloud_tools = [
        "portia:google:docs:get_structured_document", 
        "portia:google:sheets:get_spreadsheet	",
        "portia:google:drive:search	",
        "portia:google:docs:get_document"
    ]
    
    for tool in portia_cloud_registry.get_tools():
        if tool.id in desired_cloud_tools:
            cloud_tools.append(tool)
            print(f"✅ Added cloud tool: {tool.id}")
    
    # Create marketing-focused tool registry
    research_registry = ToolRegistry(local_tools + cloud_tools +current_research_registry)
    print(f"✅ Created research registry with {len(research_registry)} tools")
    return research_registry