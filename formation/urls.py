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
    path('formation/<int:formation_id>/', views.DetailFormationView.as_view(), name='formation_detail'),
    path('formation/session/<int:sessionFormation_id>/', views.DetailSessionView.as_view(), name='session_detail'),

    # New object form
    path('newFormationForm/', views.NewFormationFormView.as_view(), name='newFormationForm'),
    path('newSessionForm/<int:formation_id>', views.NewSessionFormView.as_view(), name='newSessionForm'),
    path('newRegistrationForm/', views.NewRegistrationFormView.as_view(), name='newRegistrationForm'),

    # Modification Object
    path('formation/<int:formation_id>/update', views.UpdateFormationView.as_view(), name='updateFormation'),
    path('formation/session/<int:sessionFormation_id>/update', views.UpdateSessionView.as_view(), name='updateSession'),

    # Button Inscription/Desinscription
    path('newRegistration/session/<int:session_id>/', views.registration_session, name='registrationSession'),
    path('cancelRegistration/session/<int:session_id>/', views.cancel_registration_session,
         name='cancelRegistrationSession'),

    # SuppressionFormation et SuppressionSession
    path('formation/<int:formation_id>/delete', views.FormationDeleteView.as_view(), name='deleteFormation'),
    path('formation/session/<int:sessionFormation_id>/delete', views.SessionDeleteView.as_view(), name='deleteSession'),

    # Calendar
    path('calendar/', views.CalendarView.as_view(), name='calendar'),

    # NavBar
    path('formation/formateur/<int:formateur_id>/', views.FormationListForFormateurView.as_view(),
         name='formation_list_current_formateur'),
    path('formation/student/<int:student_id>/', views.RegistrationListForStudentsView.as_view(),
         name='inscription_list_current_student'),

    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
]
