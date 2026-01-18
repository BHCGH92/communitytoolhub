from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Tool, Borrowing
from django.contrib import messages

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
    Processes a borrowing request for a specific tool.
    Checks availability, creates a Borrowing record for the current user,
    sets a 7-day return date, and marks the tool as unavailable.
    """
    tool = get_object_or_404(Tool, id=tool_id)
    
    if tool.is_available:
        return_date = timezone.now().date() + timedelta(days=7)
        
        Borrowing.objects.create(
            user=request.user,
            tool=tool,
            return_date=return_date
        )
        
        # This is the part that makes the database "care"
        tool.is_available = False
        tool.save()
        messages.success(request, f'Success! You have borrowed {tool.name}.')
        
    return redirect('tool_list')

@login_required
def return_tool(request, borrowing_id):
    """
    Handles returning a tool. Updates the borrowing record 
    and makes the tool available for others to borrow again.
    """
    borrowing = get_object_or_404(Borrowing, id=borrowing_id, user=request.user)
    
    # Change status to pending review
    borrowing.status = 'pending'
    borrowing.save()
    
    # Note: We do NOT set tool.is_available = True yet!
    
    messages.info(request, f'Thank you. {borrowing.tool.name} is now awaiting admin review.')
    return redirect('profile')