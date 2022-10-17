from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView, CreateView

from formation.forms.new_formation_form import NewFormationForm
from formation.model.Formation import Formation


class NewFormationFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'formation.add_formation'
    model = Formation
    template_name = 'formation/newFormationForm.html'
    form_class = NewFormationForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.instance.formateur = self.request.user.formateur
        return super().form_valid(form)
