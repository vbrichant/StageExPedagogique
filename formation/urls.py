from django.urls import path

from . import views

app_name = 'formation'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('newFormationForm/', views.NewFormationFormView.as_view(), name='newFormationForm')
]
