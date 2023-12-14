from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import  forms
from django.forms import ModelForm

from .models import Review,Product


#Product form #use _all_ to import all fields
class NewProduct(ModelForm):
    class Meta:
        
        model = Product
        # fields = '__all__'
        exclude = ('owner',)

#form control bootstrap css class is added to the fields below registered to django registration form

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'] = forms.ChoiceField(
            choices=[
                ('ML', 'MALE'),
                ('FM', 'FEMALE'),
                ('NA', 'NON-BINARY')
            ],
            required=True
        )
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})

class Rating(ModelForm):
    
    class Meta:
        model = Review
        exclude = ('reviewer',)

    def __init__(self, *args, **kwargs):
        super(Rating,self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'placeholder': '1 - 10'})