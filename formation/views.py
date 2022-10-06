from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.views import generic
from formation.forms import *
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class NewFormationFormView(LoginRequiredMixin, FormView):
    model = Formation, Formateur
    template_name = 'formation/newFormationForm.html'
    form_class = NewFormationForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_formation(self.request.user.formateur)
        return super().form_valid(form)


class NewSessionFormView(LoginRequiredMixin, FormView):
    model = SessionFormation
    template_name = 'formation/newSessionForm.html'
    form_class = NewSessionForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_session()
        return super().form_valid(form)


class NewInscriptionFormView(LoginRequiredMixin, FormView):
    model = Inscription
    template_name = 'formation/newInscriptionForm.html'
    fields = ('session',)
    success_url = '/formation/'
    form_class = NewInscriptionForm

    def form_valid(self, form):
        self.create_new_inscription(self.request.user.student, self.request)
        return super().form_valid(form)


# Test de Select2
class NewInscriptionCreateView(generic.CreateView):
    template_name = 'formation/newInscriptionForm.html'
    model = models.Formation
    form_class = SessionInscriptionForm
    success_url = "/"


class NewInscriptionCreateView2(generic.CreateView):
    template_name = 'formation/newInscriptionForm.html'
    model = models.Formation
    form_class = SessionInscriptionForm
    success_url = "/"


class IndexView(generic.ListView):
    template_name = 'formation/formationList.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
        return Formation.objects.all()


class DetailFormationView(generic.DetailView):
    model = Formation
    template_name = "formation/formationDetail.html"
    context_object_name = "formation_detail"

    def get_queryset(self):
        return Formation.objects.all()


class DetailSessionView(generic.DetailView):
    model = SessionFormation
    template_name = "formation/sessionDetail.html"
    context_object_name = "Session_detail"

    def get_queryset(self):
        return SessionFormation.objects.all()


class FormationListForFormateur(LoginRequiredMixin, generic.ListView):
    model = Formation
    template_name = "formation/formationList.html"
    context_object_name = "formation_list"

    def get_queryset(self):
        return Formation.objects.filter(formateur__user=self.request.user)


class InscriptionListForStudents(LoginRequiredMixin, generic.ListView):
    template_name = 'formation/inscriptionList.html'
    context_object_name = 'inscription_list'
    model = Inscription

    def get_queryset(self):
        return Inscription.objects.filter(student__user=self.request.user)


def inscription_session(request, session_id):
    print(request)
    print(session_id)
    new_inscription = Inscription(session=session_id, student=request.user.student)
    print(new_inscription)
    # new_inscription.save()
