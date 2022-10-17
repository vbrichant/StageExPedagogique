from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


class NewRegistrationForm(ModelForm):
    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super(NewRegistrationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Inscription
        fields = ('session',)

    def clean_session(self):
        inscription_set = self.cleaned_data.get('session').inscription_set.all()
        for inscription in inscription_set:
            if inscription.student == self.user.student:
                raise ValidationError(_('Vous êtes déja inscit a cette formation'))
        if self.cleaned_data.get('session').max_students <= inscription_set.count():
            raise ValidationError(_("Le nombre maximal d'étudiant inscit a cette formation est déja atteint"))
        return self.cleaned_data.get('session')
