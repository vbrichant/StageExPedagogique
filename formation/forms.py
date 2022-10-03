from django import forms

from .models import Formateur, Formation


def get_formateur_name():
    formateur_list = []
    for formateur in Formateur.objects.all():
        formateur_list.append(formateur.name)
    return formateur_list


class NewFormationForm(forms.Form):
    formation_name = forms.CharField()
    formation_description = forms.CharField(widget=forms.Textarea)

    def create_new_formation(self, user_logged):
        data = self.cleaned_data
        new_formation = Formation(name=data["formation_name"], description=data["formation_description"],
                                  formateur=user_logged)
        new_formation.save()


class NewSessionForm(forms.Form):
    formation_place = forms.CharField(max_length=50)
    formation_date = forms.DateField()
    formation_max_students = forms.IntegerField(max_value=100)

    def create_new_session(self):
        pass


class NewInscriptionForm(forms.Form):
    def create_new_inscription(self, formateur):
        pass
