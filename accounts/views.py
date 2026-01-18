from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tools.models import Borrowing

def register(request):
    """View to handle user registration."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    """View to display the user's profile and their borrowing history."""
    query = request.GET.get('pq')
    my_borrows = Borrowing.objects.filter(user=request.user).order_by('-borrowed_date')

    if query:
        my_borrows = my_borrows.filter(tool__name__icontains=query)

    context = {
        'my_borrows': my_borrows,
    }
    return render(request, 'accounts/profile.html', context)