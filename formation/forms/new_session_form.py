from django import forms
from django.contrib.auth.models import User

from formation.model.Formation import Formation
from formation.model.SessionFormation import SessionFormation


class NewSessionForm(forms.ModelForm):

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super(NewSessionForm, self).__init__(*args, **kwargs)
        self.fields['formation'].queryset = Formation.objects.filter(
            formateur__user=self.user)

    class Meta:
        model = SessionFormation
        fields = ['formation', 'place', 'date', 'time', 'max_students']
        widgets = {
            'date': forms.SelectDateWidget(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    formation = forms.ModelChoiceField(queryset=None,
                                       to_field_name='name')
    max_students = forms.IntegerField(min_value=5, max_value=150)


