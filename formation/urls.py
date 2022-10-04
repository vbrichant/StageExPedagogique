from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'formation'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('formation/<int:pk>/', views.DetailFormationView.as_view(), name='formation_detail'),
    path('session/<int:pk>/', views.DetailSessionView.as_view(), name='session_detail'),
    path('newFormationForm/', views.NewFormationFormView.as_view(), name='newFormationForm'),
    path('newSessionForm/<int:pk>', views.NewSessionFormView.as_view(), name='newSessionForm'),
    path('newInscriptionForm/', views.NewInscriptionFormView.as_view(), name='newInscriptionForm'),
    path('formation/formateur/<int:pk>/', views.FormationListForFormateur.as_view(),
         name='formation_list_current_formateur'),
    path('formation/student/<int:pk>/', views.InscriptionListForStudents.as_view(),
         name='formation_list_current_student'),
]
