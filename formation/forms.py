import contextvars
import datetime

from django import forms
from calendar import HTMLCalendar
from django.utils import timezone
from django.shortcuts import get_object_or_404

from . import models
from .models import Formateur, Formation, SessionFormation, Inscription


def get_formateur_name():
    formateur_list = []
    for formateur in Formateur.objects.all():
        formateur_list.append(formateur.get_name)
    return formateur_list


def get_formation_name_list():
    formation_list = Formation.objects.all()
    formation_list_name = []
    for formation in formation_list:
        formation_list_name.append((formation.id, formation.name))
    return formation_list_name


def get_session_name_list():
    session_list = SessionFormation.objects.all()
    session_list_name = []
    for session in session_list:
        session_list_name.append((session.id, session))
    return session_list_name


class NewFormationForm(forms.Form):
    formation_name = forms.CharField()
    formation_description = forms.CharField(widget=forms.Textarea)

    def create_new_formation(self, user_logged):
        data = self.cleaned_data
        new_formation = Formation(name=data["formation_name"], description=data["formation_description"],
                                  formateur=user_logged)
        new_formation.save()


class NewSessionForm(forms.Form):
    get_formation_name_list()
    formation_name = forms.ChoiceField(choices=get_formation_name_list())
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


class NewRegistrationForm(forms.Form):
    session_formation = forms.ChoiceField(choices=get_session_name_list())

    def create_new_registration(self, student):
        data = self.cleaned_data
        session = get_object_or_404(SessionFormation, id=data["session_formation"])
        print(data["session_formation"])
        print(session)

        new_inscription = Inscription(session=session, student=student)
        new_inscription.save()


class UpdateSessionForm(forms.Form):
    pass


class UpdateFormationForm(forms.Form):
    pass
