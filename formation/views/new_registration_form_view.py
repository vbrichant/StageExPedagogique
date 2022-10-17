from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView

from formation.forms.new_registration_form import NewRegistrationForm
from formation.model.Inscription import Inscription


class NewRegistrationFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'formation.add_inscription'
    model = Inscription
    template_name = 'formation/newRegistrationForm.html'
    success_url = '/formation/newRegistrationForm/'
    form_class = NewRegistrationForm

    def get_form_kwargs(self):
        kwargs = super(NewRegistrationFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        form.clean_session()
        messages.success(self.request, "Inscription enregistrée.")
        return super().form_valid(form)
