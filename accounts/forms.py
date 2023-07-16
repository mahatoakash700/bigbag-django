from django import forms
from .models import Account
from django.contrib import messages


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'country', 'city', 'pin_code', 'password', 'confirm_password',]

    def clean(self):
        print("cleaning")
        cleaned_data = super(RegistrationForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
