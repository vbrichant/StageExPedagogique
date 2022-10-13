import contextvars

from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Formateur, Formation, SessionFormation, Inscription, User


def get_formateur_name_list():
    formateur_list = []
    for formateur in Formateur.objects.all():
        formateur_list.append(formateur.get_name)
    return formateur_list


def get_formation_name_list():
    formation_list = Formation.objects.all()
    formation_list_name = []
    for formation in formation_list:
        if formation.formateur.user == "self.user":
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


class NewSessionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(NewSessionForm, self).__init__(*args, **kwargs)
        self.fields['formation'].queryset = Formation.objects.filter(
            formateur__user=self.request.user)

    class Meta:
        model = SessionFormation
        fields = ['formation', 'place', 'date', 'time', 'max_students']
        widgets = {
            'date': forms.SelectDateWidget(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    formation = forms.ModelChoiceField(queryset=None,
                                       to_field_name='name',
                                       widget=forms.Select)
    place = forms.CharField
    max_students = forms.IntegerField(min_value=5, max_value=150)

    def create_new_session(self):
        data = self.cleaned_data
        new_session = SessionFormation(formation_id=data["formation"].id, place=data["place"],
                                       date=data["date"], time=data["time"],
                                       max_students=data["max_students"])
        new_session.save()


class NewRegistrationForm(forms.Form):
    session_formation = forms.ChoiceField(choices=get_session_name_list())

    def create_new_registration(self, student):
        data = self.cleaned_data
        session = get_object_or_404(SessionFormation, id=data["session_formation"])
        new_inscription = Inscription(session=session, student=student)
        new_inscription.save()
