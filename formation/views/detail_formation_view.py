from django.views import generic

from formation.model.Formation import Formation


class DetailFormationView(generic.DetailView):
    model = Formation
    template_name = "formation/formationDetail.html"
    context_object_name = "formation"
    pk_url_kwarg = 'formation_id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['formation_id'])

