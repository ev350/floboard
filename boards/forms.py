from django import forms
from django.forms.widgets import TextInput
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
            'header_color': TextInput(attrs={'type': 'color'}),
        }
