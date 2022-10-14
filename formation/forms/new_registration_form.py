
from django import forms
from django.shortcuts import get_object_or_404

from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


class NewRegistrationForm(forms.Form):
    class Meta:
        model = SessionFormation

    session_formation = forms.ModelChoiceField(queryset=SessionFormation.objects.all())

    def create_new_registration(self, student):
        data = self.cleaned_data
        session = get_object_or_404(SessionFormation, id=data["session_formation"])
        new_inscription = Inscription(session=session, student=student)
        new_inscription.save()
