from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'include country code'}))
    class Meta:
        model = Task
        exclude = ('taskedby',)