import calendar
import datetime
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from formation.forms import *
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


class NewRegistrationFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'formation.add_inscription'
    model = Inscription
    template_name = 'formation/newRegistrationForm.html'
    success_url = '/formation/newRegistrationForm/'
    form_class = NewRegistrationForm

    def form_valid(self, form):
        session = get_object_or_404(SessionFormation, id=form.cleaned_data["session_formation"])
        if self.request.user.id in session.get_students_registered():
            messages.error(self.request,
                           "Vous êtes déjà inscrit à cette session")
        elif session.get_count_registration() > session.max_students:
            messages.error(self.request,
                           "Le nombre d'inscription maximum est déjà atteint, Choisissez une autre session.")
        else:
            form.create_new_registration(self.request.user.student)
            messages.success(self.request, "Inscription enregistrée.")
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
    template_name = 'formation/index.html'
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


class RegistrationListForStudentsView(LoginRequiredMixin, generic.ListView):
    template_name = 'formation/registrationList.html'
    context_object_name = 'registration_list'
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
def registration_session(request, session_id):
    session = get_object_or_404(SessionFormation, pk=session_id)
    print(request.user)
    user = request.user
    if session.get_count_registration() < session.max_students:
        new_inscription = Inscription(session=session, student=user.student)
        new_inscription.save()
        return HttpResponseRedirect(reverse('formation:inscription_list_current_student', args=(user.student.id,)))
    else:
        messages.error(request, "Le nombre d'inscription maximum est déjà atteint, Choisissez une autre session.")
        return HttpResponseRedirect(reverse('formation:formation_detail', args=(session.formation.id,)))


@login_required
@permission_required('formation.add_inscription', raise_exception=True)
def cancel_registration_session(request, session_id):
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
        d = get_date(self.request.GET.get('month', None))
        calendar_object = Calendar()
        html_calendar = calendar_object.formatmonth(theyear=d.year, themonth=d.month, withyear=True)
        context['calendar'] = mark_safe(html_calendar)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    previous_month_object = first - timedelta(days=1)
    month = 'month=' + str(previous_month_object.year) + '-' + str(previous_month_object.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month_object = last + timedelta(days=1)
    month = 'month=' + str(next_month_object.year) + '-' + str(next_month_object.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.date.today()
