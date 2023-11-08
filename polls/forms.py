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

class RegistrationForm(UserCreationForm):
    Sex = (
    ("ML","MALE"),
    ("FM", "FEMALE"),
    ("NA", "NON-BINARY")
    )
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'class':'form-control'}))
    gender =  forms.ChoiceField(choices=Sex )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2')

#this fucntion allows adding bootstrap class form to fields named form control
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class Rating(ModelForm):
    
    class Meta:
        model = Review
        exclude = ('reviewer',)

    def __init__(self, *args, **kwargs):
        super(Rating,self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'placeholder': '1 - 10'})