from django.views import generic

from formation.model.Formation import Formation


class FormationListView(generic.ListView):
    template_name = 'formation/index.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
        return Formation.objects.all()
