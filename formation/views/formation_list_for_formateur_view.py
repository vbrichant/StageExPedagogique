from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from formation.model.Formation import Formation


class FormationListForFormateurView(LoginRequiredMixin, generic.ListView):
    model = Formation
    template_name = "formation/formationList.html"
    context_object_name = "formation_list"

    def get_queryset(self):
        return Formation.objects.filter(formateur__user=self.request.user)

