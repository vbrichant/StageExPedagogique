from django.urls import path, include
from django.contrib.auth import views as auth_views
from schema_graph.views import Schema

from . import views

app_name = 'formation'
urlpatterns = [
    path('', views.FormationListView.as_view(), name='formation_list'),
    # path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('select2/', include('django_select2.urls')),
    # URL Formation APP

    # Detail view
    path('formation/<int:pk>/', views.DetailFormationView.as_view(), name='formation_detail'),
    path('session/<int:pk>/', views.DetailSessionView.as_view(), name='session_detail'),

    # New object form
    path('newFormationForm/', views.NewFormationFormView.as_view(), name='newFormationForm'),
    path('newSessionForm/<int:pk>', views.NewSessionFormView.as_view(), name='newSessionForm'),
    path('newInscriptionForm/', views.NewInscriptionFormView.as_view(), name='newInscriptionForm'),

    # Modification Object
    path('formation/<int:pk>/update', views.UpdateFormationView.as_view(), name='updateFormation'),
    path('formation/session/<int:pk>/update', views.UpdateSessionView.as_view(), name='updateSession'),

    # Button Inscription/Desinscription
    path('newInscription/session/<int:session_id>/', views.inscription_session, name='inscriptionSession'),
    path('Desinscription/session/<int:session_id>/', views.desinscription_session, name='desinscriptionSession'),

    # SuppressionFormation et SuppressionSession
    path('formation/<int:pk>/delete', views.FormationDeleteView.as_view(), name='deleteFormation'),
    path('formation/session/<int:pk>/delete', views.SessionDeleteView.as_view(), name='deleteSession'),

    # Calendar
    path('calendar/', views.CalendarView.as_view(), name='calendar'),

    # NavBar
    path('formation/formateur/<int:pk>/', views.FormationListForFormateurView.as_view(),
         name='formation_list_current_formateur'),
    path('formation/student/<int:pk>/', views.InscriptionListForStudentsView.as_view(),
         name='inscription_list_current_student'),

    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
]
