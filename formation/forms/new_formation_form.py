from django import forms

from formation.model.Formation import Formation


class NewFormationForm(forms.Form):
    formation_name = forms.CharField()
    formation_description = forms.CharField(widget=forms.Textarea)

    def create_new_formation(self, user_logged):
        data = self.cleaned_data
        new_formation = Formation(name=data["formation_name"], description=data["formation_description"],
                                  formateur=user_logged)
        new_formation.save()
