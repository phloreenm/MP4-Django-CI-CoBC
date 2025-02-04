from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county', 'comments'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name', 'autocomplete': 'on'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'autocomplete': 'on'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'autocomplete': 'on'}),
            'street_address1': forms.TextInput(attrs={'placeholder': 'Street Address 1', 'autocomplete': 'on'}),
            'street_address2': forms.TextInput(attrs={'placeholder': 'Street Address 2', 'autocomplete': 'on'}),
            'town_or_city': forms.TextInput(attrs={'placeholder': 'Town or City', 'autocomplete': 'on'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postal Code', 'autocomplete': 'on'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country', 'autocomplete': 'on'}),
            'county': forms.TextInput(attrs={'placeholder': 'County', 'autocomplete': 'on'}),
            'comments': forms.Textarea(attrs={'placeholder': 'Additional comments', 'autocomplete': 'on'}),
        }

class OrderLookupForm(forms.Form):
    order_number = forms.CharField(
        max_length=32,
        label="Order Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your Order Number',
            'autofocus': True,
            'autocomplete': 'on'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter the email used at checkout',
            'autocomplete': 'on'
        })
    )