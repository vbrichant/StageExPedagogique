from django.db.models import Prefetch, Count, Subquery, OuterRef, Exists
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
            'formation__formateur__user',
        ).annotate(
            inscription_count=Count('inscription'),
            already_regitered=Exists(
                Inscription.objects.filter(
                    session_id=OuterRef("id"),
                    student__user_id=self.request.user.pk
                )
            ))
        print(queryset.first().already_regitered)
        return queryset
    # ,students_ids_registered=
