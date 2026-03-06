from django import forms
from .models import Hostel, Review

class HostelSearchForm(forms.Form):
    """Form for searching hostels"""
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)

class ReviewForm(forms.ModelForm):
    """Form for hostel reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience...',
                'class': 'form-control'
            }),
        }