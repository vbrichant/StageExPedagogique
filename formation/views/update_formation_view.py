from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation.model.Formation import Formation


class UpdateFormationView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'formation.change_formation'
    model = Formation
    fields = ['name', 'description']
    template_name = 'formation/newFormationForm.html'
    success_url = "/formation/"
    pk_url_kwarg = "formation_id"