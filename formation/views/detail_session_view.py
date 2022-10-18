from django.db.models import Prefetch
from django.views import generic

from formation.model.Formation import Formation
from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


class DetailSessionView(generic.DetailView):
    model = SessionFormation
    template_name = "formation/sessionDetail.html"
    context_object_name = "session_formation"
    pk_url_kwarg = 'sessionFormation_id'

    def get_queryset(self):
        queryset = SessionFormation.objects.filter(id=self.kwargs['sessionFormation_id']).select_related(
            'formation__formateur__user',).prefetch_related(
            Prefetch(
                'inscription_set'
            ),
        )
        return queryset
