from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView

from formation.forms.new_session_form import NewSessionForm
from formation.model.SessionFormation import SessionFormation


class NewSessionFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_sessionformation'
    model = SessionFormation
    template_name = 'formation/newSessionForm.html'
    form_class = NewSessionForm
    success_url = '/formation/'

    def get_form_kwargs(self):

        kwargs = super(NewSessionFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.create_new_session()
        return super().form_valid(form)
