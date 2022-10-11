from datetime import date

from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

# Create your views here.
from django.views import generic
from formation.forms import *
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from formation.utils import Calendar


##
# FormView
##
class NewFormationFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_formation'
    model = Formation, Formateur
    template_name = 'formation/newFormationForm.html'
    form_class = NewFormationForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_formation(self.request.user.formateur)
        return super().form_valid(form)


class NewSessionFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_sessionformation'
    model = SessionFormation
    template_name = 'formation/newSessionForm.html'
    form_class = NewSessionForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_session()
        return super().form_valid(form)


class NewInscriptionFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_inscription'
    model = Inscription
    template_name = 'formation/newInscriptionForm.html'
    success_url = '/formation/'
    form_class = NewInscriptionForm

    def form_valid(self, form):
        form.create_new_inscription(self.request.user.student)
        return super().form_valid(form)


##
# DetailView
##
class DetailFormationView(generic.DetailView):
    model = Formation
    template_name = "formation/formationDetail.html"
    context_object_name = "formation"

    def get_queryset(self):
        return Formation.objects.all()


class DetailSessionView(generic.DetailView):
    model = SessionFormation
    template_name = "formation/sessionDetail.html"
    context_object_name = "session"

    def get_queryset(self):
        return SessionFormation.objects.all()


##
# ListView
##
class FormationListView(generic.ListView):
    template_name = 'formation/formationList.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
        return Formation.objects.all()


class FormationListForFormateurView(LoginRequiredMixin, generic.ListView):
    model = Formation
    template_name = "formation/formationList.html"
    context_object_name = "formation_list"

    def get_queryset(self):
        return Formation.objects.filter(formateur__user=self.request.user)


class InscriptionListForStudentsView(LoginRequiredMixin, generic.ListView):
    template_name = 'formation/inscriptionList.html'
    context_object_name = 'inscription_list'
    model = Inscription

    def get_queryset(self):
        return Inscription.objects.filter(student__user=self.request.user)


##
# UpdateView
##
class UpdateFormationView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'formation.change_formation'
    model = Formation
    fields = ['name', 'description']
    template_name = 'formation/newFormationForm.html'
    success_url = "/formation/"


class UpdateSessionView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'formation.change_sessionformation'
    model = SessionFormation
    fields = ["formation", "date", "place", "max_students"]
    template_name = 'formation/newSessionForm.html'
    success_url = "/formation/"


##
# Suppression (Formation et Session)
##
class FormationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'formation.delete_formation'
    model = Formation
    success_url = "/formation/"
    template_name = "formation/formationConfirmDelete.html"


class SessionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'formation.delete_sessionformation'
    model = SessionFormation
    success_url = "/formation/"
    template_name = "formation/sessionConfirmDelete.html"


###
# Inscription/Desinscription
###
@login_required
@permission_required('formation.add_inscription', raise_exception=True)
def inscription_session(request, session_id):
    session = get_object_or_404(SessionFormation, pk=session_id)
    user = request.user
    new_inscription = Inscription(session=session, student=user.student)
    new_inscription.save()
    return HttpResponseRedirect(reverse('formation:inscription_list_current_student', args=(user.student.id,)))


@login_required
@permission_required('formation.add_inscription', raise_exception=True)
def desinscription_session(request, session_id):
    session = get_object_or_404(SessionFormation, pk=session_id)
    student = request.user.student
    inscription = get_object_or_404(Inscription, session=session, student=student)
    print(inscription)
    inscription.delete()
    return HttpResponseRedirect(reverse('formation:inscription_list_current_student', args=(student.id,)))


##
# Calendrier
##

class CalendarView(generic.ListView):
    model = SessionFormation
    template_name = 'formation/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        # Instantiate our calendar class with today's year and date
        calendar = Calendar()
        # Call the formatmonth method, which returns our calendar as a table
        html_calendar = calendar.formatmonth(theyear=d.year, themonth=d.month, withyear=True)
        context['calendar'] = mark_safe(html_calendar)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.date.today()
