from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation.model.SessionFormation import SessionFormation


class SessionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'formation.delete_sessionformation'
    model = SessionFormation
    success_url = "/formation/"
    template_name = "formation/sessionConfirmDelete.html"
    pk_url_kwarg = "sessionFormation_id"
