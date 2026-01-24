from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Tool, Borrowing
from django.contrib import messages
from django.db.models import Q
import stripe
from django.conf import settings
from checkout.views import create_checkout_session, payment_success, payment_cancel, stripe_webhook

def all_tools(request):
    """ 
    A view to show all tools, including sorting, search queries, and pagination.
    """
    tools_list = Tool.objects.all().order_by('-id') 
    query = request.GET.get('q')

    if query:
        tools_list = tools_list.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query)
        )

    paginator = Paginator(tools_list, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_term': query,
    }
    return render(request, 'tools/tools.html', context)

def tool_detail(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        selected_date_str = request.POST.get('borrow_date')
        if selected_date_str:
            total_price = tool.price_per_day * 7
            stripe_total = int(total_price * 100) 

            request.session['pending_borrow_date'] = selected_date_str
            
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'gbp',
                            'unit_amount': stripe_total,
                            'product_data': {
                                'name': f"{tool.name} (7-Day Rental)",
                                'description': f"Collection Date: {selected_date_str}",
                            },
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(f'/tools/payment-success/{tool.id}/'),
                    cancel_url=request.build_absolute_uri(f'/tools/{tool.id}/'),
                )
                return redirect(checkout_session.url, code=303)
            except Exception as e:
                messages.error(request, "Stripe connection failed. Please try again.")

    return render(request, 'tools/tool_detail.html', {'tool': tool})

@login_required
def return_tool(request, borrowing_id):
    """
    Handles returning a tool. Updates the borrowing record 
    and makes the tool available for others to borrow again.
    """
    borrowing = get_object_or_404(Borrowing, id=borrowing_id, user=request.user)
    borrowing.status = 'pending'
    borrowing.save()
    
    messages.info(request, f'Thank you. {borrowing.tool.name} is now awaiting admin review.')
    return redirect('profile')

def resolve_dispute(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)

    if request.method == 'POST':
        user_reason = request.POST.get('reason')
        
        if user_reason:
            borrowing.status = 'pending'
            borrowing.user_notes = user_reason 
            borrowing.save()
            
            messages.success(request, "Your response has been submitted for review.")
        else:
            messages.error(request, "Please provide a reason for the resolution.")

    return redirect('profile_view')

def error_404(request, exception):
    """ Handles 404 - Page Not Found """
    context = {
        'status_code': 404,
        'error_title': 'Oops! Tool Not Found',
        'error_message': 'It looks like you followed a broken link or typed in a URL that doesn\'t exist in our hub.'
    }
    return render(request, 'errors/error.html', context, status=404)

def error_500(request):
    """ Handles 500 - Server Error """
    context = {
        'status_code': 500,
        'error_title': 'System Glitch',
        'error_message': 'Our server ran into a snag. Don\'t worry, our team is looking into it.'
    }
    return render(request, 'errors/error.html', context, status=500)