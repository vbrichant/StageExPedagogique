from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import *
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'formation/index.html'
    context_object_name = 'formation_list'

    def get_queryset(self):
        """Return all formation not close"""
        return Formation.objects.all()


class NewFormationFormView(generic.DetailView):
    model = Formation
    template_name = 'formation/newFormationForm.html'
