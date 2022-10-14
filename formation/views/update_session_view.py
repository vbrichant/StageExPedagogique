from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation.model.SessionFormation import SessionFormation


class UpdateSessionView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'formation.change_sessionformation'
    model = SessionFormation
    fields = ["formation", "date", "place", "max_students"]
    template_name = 'formation/newSessionForm.html'
    success_url = "/formation/"
    pk_url_kwarg = "sessionFormation_id"