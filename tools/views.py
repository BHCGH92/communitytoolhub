from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Tool, Borrowing

def all_tools(request):
    """ 
    A view to show all tools, including sorting and search queries.
    """
    tools = Tool.objects.all()
    context = {
        'tools': tools,
    }
    return render(request, 'tools/tools.html', context)

class ToolDetailView(DetailView):
    """
    Renders a detailed view for a specific tool instance,
    including its description, image, and availability.
    """
    model = Tool
    template_name = 'tools/tool_detail.html'
    context_object_name = 'tool'

@login_required
def borrow_tool(request, tool_id):
    """
    Handles the logic for borrowing a tool.
    Creates a Borrowing record for the logged-in user.
    """
    tool = get_object_or_404(Tool, id=tool_id)
    
    return_date = timezone.now().date() + timedelta(days=7)
    
    Borrowing.objects.create(
        user=request.user,
        tool=tool,
        return_date=return_date
    )
    
    return redirect('tool_list')