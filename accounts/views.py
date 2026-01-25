from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tools.models import Borrowing
from django.utils import timezone
from django.core.paginator import Paginator


def register(request):
    """View to handle user registration."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success
            (request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """View to display the user's profile with
    search, status filters, and pagination."""
    query = request.GET.get('pq')
    status_filter = request.GET.get('status')

    my_borrows = Borrowing.objects.filter(user=request.user).order_by('-id')

    if query:
        my_borrows = my_borrows.filter(tool__name__icontains=query)
    if status_filter and status_filter != 'all':
        my_borrows = my_borrows.filter(status=status_filter)

    paginator = Paginator(my_borrows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'borrowings': page_obj,
        'today': timezone.now().date(),
        'search_term': query,
        'current_status': status_filter,
    }
    return render(request, 'accounts/profile.html', context)
