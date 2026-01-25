from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    """
    Form to register a new user and capture initial profile data.
    """
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    town_or_city = forms.CharField(max_length=40, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Update the profile created by my signal
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.town_or_city = self.cleaned_data.get('town_or_city')
            profile.save()
        return user
