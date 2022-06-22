import imp
from django import forms
from .models import Order


class CheckOutForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Order
        exclude = ("quantity", "product", "price")

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "address1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "address1"}
            ),
            "address2": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "address2 "}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "country"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "state"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "zip_code"}
            ),
        }
