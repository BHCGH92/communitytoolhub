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
    """
    Displays the user's profile and a list of their borrowed tools.
    """
    my_borrows = Borrowing.objects.filter(user=request.user).order_by('-borrowed_date')
    
    context = {
        'my_borrows': my_borrows,
    }
    return render(request, 'accounts/profile.html', context)