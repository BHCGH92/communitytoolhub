import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from tools.models import Tool, Borrowing
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, tool_id):
    """ Creates a Stripe session for a specific tool with a 7-day minimum """
    tool = get_object_or_404(Tool, id=tool_id)
    
    if not tool.is_available:
        messages.error(request, "Sorry, this tool was just grabbed by someone else!")
        return redirect('tool_detail', pk=tool.id)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            # METADATA: Crucial for the webhook to identify the user and tool
            metadata={
                'tool_id': tool.id,
                'user_id': request.user.id
            },
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': f"Rental: {tool.name} (7-Day Minimum)",
                    },
                    'unit_amount': int(tool.price_per_day * 100),
                },
                'quantity': 7,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + f"?tool_id={tool.id}",
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, "Payment gateway error. Please try again.")
        return redirect('tool_detail', pk=tool.id)

def payment_success(request):
    tool_id = request.GET.get('tool_id')
    tool = get_object_or_404(Tool, id=tool_id)
    
    # GUARD Clause: Check if the tool is still actually available
    # We use select_for_update() to 'lock' the row during this check...
    try:
        with transaction.atomic():
            # Refresh the tool data from the DB to be 100% sure of its status
            tool_to_lock = Tool.objects.select_for_update().get(id=tool.id)
            
            if not tool_to_lock.is_available:
                # Check if the webhook already processed this
                already_borrowed = Borrowing.objects.filter(
                    tool=tool_to_lock, 
                    user=request.user, 
                    status='active'
                ).exists()
                
                if already_borrowed:
                    return render(request, 'payment_success.html', {'tool': tool})

                messages.error(request, "Too late! Someone else finished their payment just before you. Please contact support for a refund.")
                return redirect('tool_list')

            # 2. SUCCESS PATH: Create the record
            return_date = timezone.now().date() + timedelta(days=7)
            Borrowing.objects.create(
                user=request.user,
                tool=tool_to_lock,
                return_date=return_date,
                status='active'
            )
            
            # 3. Mark as unavailable immediately
            tool_to_lock.is_available = False
            tool_to_lock.save()

    except Exception as e:
        messages.error(request, "A system error occurred. Please contact support.")
        return redirect('tool_list')
    
    messages.success(request, f"Payment Confirmed! {tool.name} is now reserved for you.")
    return render(request, 'payment_success.html', {'tool': tool})

def payment_cancel(request):
    """ Handles cases where the user cancels the payment process """
    messages.warning(request, "Payment cancelled. The tool has not been borrowed.")
    return render(request, 'payment_cancel.html')

@csrf_exempt
def stripe_webhook(request):
    """
    Handles background payment confirmation. 
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET 

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Extract metadata
        tool_id = session.get('metadata', {}).get('tool_id')
        user_id = session.get('metadata', {}).get('user_id')
        
        if tool_id and user_id:
            finalize_checkout(tool_id, user_id)

    return HttpResponse(status=200)

def finalize_checkout(tool_id, user_id):
    try:
        # Explicitly convert to int to prevent lookup crashes
        u_id = int(user_id)
        t_id = int(tool_id)
        
        user = User.objects.get(id=u_id)
        
        with transaction.atomic():
            tool = Tool.objects.select_for_update().get(id=t_id)
            
            if tool.is_available:
                return_date = timezone.now().date() + timedelta(days=7)
                Borrowing.objects.get_or_create(
                    user=user,
                    tool=tool,
                    status='active',
                    defaults={'return_date': return_date}
                )
                tool.is_available = False
                tool.save()
    except Exception as e:
        # This prevents a 500 and lets you see the error in Heroku logs
        print(f"WEBHOOK ERROR: {e}")