from django.forms import ModelForm
from center.models import User
from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class SignUp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        labels = {field: '' for field in fields}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class CreatePet(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["status", "name", "age", "breed", "description"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

            self.fields["name"].widget.attrs.update({
                "placeholder": "Pet name"
            })
            self.fields["age"].widget.attrs.update({
                "placeholder": "age"
            })
            self.fields["breed"].widget.attrs.update({
                "placeholder": "breed"
            })
            self.fields["description"].widget.attrs.update({
                "placeholder": "description"
            })
            self.fields["status"].widget.attrs.update({
                "placeholder": "state"
            })