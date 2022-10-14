from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from formation.model.Inscription import Inscription


class RegistrationListForStudentsView(LoginRequiredMixin, generic.ListView):
    template_name = 'formation/registrationList.html'
    context_object_name = 'registration_list'
    model = Inscription

    def get_queryset(self):
        return Inscription.objects.filter(student__user=self.request.user)

