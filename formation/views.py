from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import *
from django.views import generic
from formation.forms import *
from django.views.generic.edit import FormView
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
    form_class = NewInscriptionForm
    success_url = '/formation/'

    def form_valid(self, form):
        form.create_new_inscription(self.request.user.student)
        return super().form_valid(form)


class IndexView(generic.ListView):
    template_name = 'formation/formationList.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
        # print(Formateur.objects.all().values('user__username', 'user_id'))
        return Formation.objects.all()


class DetailFormationView(generic.DetailView):
    model = Formation
    template_name = "formation/formation_detail.html"
    context_object_name = "formation_detail"

    def get_queryset(self):
        return Formation.objects.all()


class DetailSessionView(generic.DetailView):
    model = SessionFormation
    template_name = "formation/session_detail.html"
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
