from django import forms

class BookingForm(forms.Form):
    name    = forms.CharField(required=True)
    address = forms.CharField(required=True)
    numero  = forms.CharField(required=True)
    email   = forms.EmailField(required=True)
    option  = forms.CharField(required=True)
    comment = forms.CharField(required=False)
