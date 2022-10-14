from django.views import generic

from formation.model.SessionFormation import SessionFormation


class DetailSessionView(generic.DetailView):
    model = SessionFormation
    template_name = "formation/sessionDetail.html"
    context_object_name = "session"
    pk_url_kwarg = 'sessionFormation_id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['sessionFormation_id'])


##