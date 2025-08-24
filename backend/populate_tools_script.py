import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Sector, ToolsModel

def populate_research_tools():
    print("🔬 Starting to populate research tools...")
    
    # Get or create research sector
    research_sector, created = Sector.objects.get_or_create(
        slug='research-development',
        defaults={
            'name': 'Research & Development',
            'description': 'Advanced AI-powered Research & Development services that accelerate innovation through intelligent literature review, competitive analysis, experimental design, and data-driven insights.',
            'category': 'technology',
            'is_active': True,
            'is_featured': True,
            'order': 2
        }
    )
    
    print(f"📁 Research sector: {research_sector.name}")
    
    # Research tool definitions
    research_tools_data = [
        # Core Research Tools
        ('Search Tool', 'search_tool', 'Internet research and comprehensive literature review capabilities'),
        ('Advanced Search Tool', 'portia:tavily::search', 'Advanced search with deep web crawling and analysis'),
        ('Crawl Tool', 'crawl_tool', 'Deep website analysis and systematic data collection for research'),
        ('Extract Tool', 'extract_tool', 'Content extraction from research papers, patents, and documents'),
        ('LLM Tool', 'llm_tool', 'AI-powered analysis, summarization, and research synthesis'),
        
        # Document & File Management
        ('File Reader Tool', 'file_reader_tool', 'Read and analyze research documents, papers, and datasets'),
        ('File Writer Tool', 'file_writer_tool', 'Generate research reports, documentation, and data files'),
        ('Google Docs Reader', 'portia:google:docs:get_document', 'Access and analyze Google Docs research documents'),
        ('Structured Docs Reader', 'portia:google:docs:get_structured_document', 'Extract structured data from research documents'),
        ('Google Drive Search', 'portia:google:drive:search', 'Find research files, datasets, and documentation'),
        
        # Data Analysis & Computation
        ('Google Sheets Access', 'portia:google:sheets:get_spreadsheet', 'Access research data and analytics spreadsheets'),
        ('Calculator Tool', 'calculator_tool', 'Statistical calculations and mathematical analysis for research'),
        ('Image Understanding Tool', 'image_understanding_tool', 'Analyze research charts, graphs, diagrams, and scientific images'),
    ]
    
    created_count = 0
    for name, tool_id, description in research_tools_data:
        tool, created = ToolsModel.objects.get_or_create(
            tool_id=tool_id,
            defaults={
                'name': name,
                'description': description,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            tool.sectors.add(research_sector)
            print(f"✅ Created: {name}")
            created_count += 1
        else:
            if not tool.sectors.filter(id=research_sector.id).exists():
                tool.sectors.add(research_sector)
            print(f"🔄 Associated with R&D: {name}")
    
    print(f"\n📊 Summary:")
    print(f"   • Created {created_count} new research tools")
    print(f"   • Total R&D tools: {research_sector.toolsmodel_set.count()}")
    print("🧪 Research & Development tools population completed!")

if __name__ == "__main__":
    populate_research_tools()