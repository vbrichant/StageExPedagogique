from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation.model.Formation import Formation


class FormationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'formation.delete_formation'
    model = Formation
    success_url = "/formation/"
    template_name = "formation/formationConfirmDelete.html"
    pk_url_kwarg = "formation_id"

