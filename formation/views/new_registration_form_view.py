from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from formation.forms.new_registration_form import NewRegistrationForm
from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


class NewRegistrationFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_inscription'
    model = Inscription
    template_name = 'formation/newRegistrationForm.html'
    success_url = '/formation/newRegistrationForm/'
    form_class = NewRegistrationForm

    def form_valid(self, form):
        session = get_object_or_404(SessionFormation, id=form.cleaned_data["session_formation"])
        if self.request.user.id in session.get_students_registered():
            messages.error(self.request,
                           "Vous êtes déjà inscrit à cette session")
        elif session.get_count_registration() > session.max_students:
            messages.error(self.request,
                           "Le nombre d'inscription maximum est déjà atteint, Choisissez une autre session.")
        else:
            form.create_new_registration(self.request.user.student)
            messages.success(self.request, "Inscription enregistrée.")
        return super().form_valid(form)

