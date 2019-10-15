from django import forms


class UrbanAcroForm(forms.Form):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    option = forms.CharField(required=False)
    comment = forms.CharField(required=False)


class WinterAcroForm(forms.Form):
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    option = forms.CharField(required=False)
    allergies = forms.CharField(required=False)
    donation = forms.CharField(required=False)
    date = forms.DateField(required=False)
