from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Borrowing


class BorrowingForm(forms.Form):
    borrow_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Collection Date'
    )

    def __init__(self, *args, tool=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool = tool
        self.user = user

    def clean_borrow_date(self):
        borrow_date = self.cleaned_data['borrow_date']
        today = timezone.now().date()
        max_date = today + timedelta(days=5)

        if borrow_date < today:
            raise forms.ValidationError("Collection date cannot be in the past.")
        if borrow_date > max_date:
            raise forms.ValidationError("Collection date must be within the next 5 days.")

        return borrow_date

    def clean(self):
        cleaned_data = super().clean()

        if self.tool and not self.tool.is_available:
            raise forms.ValidationError(
                "This tool is no longer available for borrowing."
            )

        if self.tool and self.user and self.user.is_authenticated:
            already_borrowed = Borrowing.objects.filter(
                user=self.user,
                tool=self.tool,
                status='active'
            ).exists()
            if already_borrowed:
                raise forms.ValidationError(
                    "You already have an active borrowing for this tool."
                )

        return cleaned_data


class DisputeForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the issue or resolution...', 'minlength': '20', 'maxlength': '500'}),
        min_length=20,
        max_length=500,
        label='Your Response'
    )
