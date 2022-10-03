from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import *
from django.views import generic
from formation.forms import NewFormationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin


class NewFormationFormView(LoginRequiredMixin, FormView):
    model = Formation, Formateur
    template_name = 'formation/newFormationForm.html'
    form_class = NewFormationForm
    success_url = '/formation/index'

    def form_valid(self, form):
        form.create_new_formation()
        return super().form_valid(form)


class IndexView(generic.ListView):
    template_name = 'formation/index.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
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
