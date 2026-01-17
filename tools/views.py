from django.shortcuts import render
from django.views.generic import DetailView
from .models import Tool

def all_tools(request):
    """ 
    A view to show all tools, including sorting and search queries.
    """
    # 1. Fetch all tool objects from the database
    tools = Tool.objects.all()

    # 2. Define the context (the data being sent to the template)
    context = {
        'tools': tools,
    }

    # 3. Return the render function with the template path
    return render(request, 'tools/tools.html', context)

class ToolDetailView(DetailView):
    """
    Renders a detailed view for a specific tool instance,
    including its description, image, and availability.
    """
    model = Tool
    template_name = 'tools/tool_detail.html'
    context_object_name = 'tool'