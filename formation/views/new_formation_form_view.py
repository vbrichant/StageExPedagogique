from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView

from formation.forms.new_formation_form import NewFormationForm
from formation.model.Formation import Formation


class NewFormationFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_formation'
    model = Formation
    template_name = 'formation/newFormationForm.html'
    form_class = NewFormationForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_formation(self.request.user.formateur)
        return super().form_valid(form)
