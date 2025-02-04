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