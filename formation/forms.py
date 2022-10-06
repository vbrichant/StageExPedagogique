import contextvars
import datetime

from django import forms
from django.utils import timezone
from django_select2 import forms as s2forms
from django_select2.forms import Select2Widget, ModelSelect2Widget

from . import models
from .models import Formateur, Formation, SessionFormation, Inscription


def get_formateur_name():
    formateur_list = []
    for formateur in Formateur.objects.all():
        formateur_list.append(formateur.name)
    return formateur_list


def get_formation_name():
    formation_list = Formation.objects.all()
    formation_list_name = []
    for formation in formation_list:
        formation_list_name.append((formation.id, formation.name))
    return formation_list_name


class NewFormationForm(forms.Form):
    formation_name = forms.CharField()
    formation_description = forms.CharField(widget=forms.Textarea)

    def create_new_formation(self, user_logged):
        data = self.cleaned_data
        new_formation = Formation(name=data["formation_name"], description=data["formation_description"],
                                  formateur=user_logged)
        new_formation.save()


class NewSessionForm(forms.Form):
    print()
    get_formation_name()
    formation_name = forms.ChoiceField(choices=get_formation_name())
    formation_place = forms.CharField(max_length=50)
    formation_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                         initial=timezone.now())
    formation_max_students = forms.IntegerField(widget=forms.NumberInput, min_value=5, max_value=100)

    def create_new_session(self):
        data = self.cleaned_data
        new_session = SessionFormation(formation_id=data["formation_name"], place=data["formation_place"],
                                       date=data["formation_date"],
                                       max_students=data["formation_max_students"])
        new_session.save()


class NewInscriptionForm(forms.Form):
    formation_name = forms.ChoiceField(choices=get_formation_name())
    session_formation = forms.ChoiceField()

    def create_new_inscription(self, student):
        data = self.cleaned_data
        new_inscription = Inscription(session=data["session_formation"], student=student)
        new_inscription.save()


# Select2FromModels


class FormationNameWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name",
    ]


class SessionNameWidget(s2forms.ModelSelect2Widget):
    autocomplete_fields = [
        "session",
    ]


class SessionInscriptionForm2(forms.ModelForm):
    class Meta:
        model = SessionFormation
        fields = "formation", "place"
        widgets = {
            "Formation": FormationNameWidget,
            "Session": SessionNameWidget,
        }
        fields


class SessionInscriptionForm(forms.Form):
    formation = forms.ModelChoiceField(
        queryset=Formation.objects.all(),
        label="Formation",
        widget=ModelSelect2Widget(
            model=Formation,
            select_fields=['name'],
        )
    )
    session = forms.ModelChoiceField(
        queryset=SessionFormation.objects.all(),
        label="Session",
        widget=ModelSelect2Widget(
            model=SessionFormation,
            select_fields=['formation'],
            dependent_fields={'formation': 'formation'},
            max_results=500,
        )
    )



