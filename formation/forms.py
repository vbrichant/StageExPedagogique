from django import forms
from django.contrib.auth import authenticate, login

from .models import Formateur, Formation


def get_formateur_name():
    formateur_list = []
    for formateur in Formateur.objects.all():
        formateur_list.append(formateur.name)
    return formateur_list


class NewFormationForm(forms.Form):
    formation_name = forms.CharField()
    formation_description = forms.CharField(widget=forms.Textarea)
    formateur_name = forms.ModelChoiceField(queryset=Formateur.objects.all())

    def create_new_formation(self):
        data = self.cleaned_data
        new_formation = Formation(name=data["formation_name"], description=data["formation_description"],
                                  formateur=data["formateur_name"])
        new_formation.save()


