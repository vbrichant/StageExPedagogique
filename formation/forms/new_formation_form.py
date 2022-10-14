from django import forms
from django.forms import ModelForm

from formation.model.Formation import Formation


class NewFormationForm(ModelForm):
    class Meta:
        model = Formation
        fields = ('name', 'description')