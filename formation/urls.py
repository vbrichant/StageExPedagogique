from django.urls import path, include
from django.contrib.auth import views as auth_views
from schema_graph.views import Schema

from formation import views

app_name = 'formation'
urlpatterns = [

    path('accounts/login/',
         auth_views.LoginView.as_view()),
    # URL Formation APP
    path('',
         views.formation_list_view.FormationListView.as_view(),
         name='formation_list'),

    # Detail view
    path('formation/<int:formation_id>/',
         views.detail_formation_view.DetailFormationView.as_view(),
         name='formation_detail'),
    path('formation/session/<int:sessionFormation_id>/',
         views.detail_session_view.DetailSessionView.as_view(),
         name='session_detail'),

    # New object form
    path('newFormationForm/',
         views.new_formation_form_view.NewFormationFormView.as_view(),
         name='newFormationForm'),
    path('newSessionForm/<int:formation_id>/',
         views.new_session_form_view.NewSessionFormView.as_view(),
         name='newSessionForm'),
    path('newRegistrationForm/',
         views.new_registration_form_view.NewRegistrationFormView.as_view(),
         name='newRegistrationForm'),

    # Modification Object
    path('formation/<int:formation_id>/update/',
         views.update_formation_view.UpdateFormationView.as_view(),
         name='updateFormation'),
    path('formation/session/<int:sessionFormation_id>/update/',
         views.update_session_view.UpdateSessionView.as_view(),
         name='updateSession'),

    # Button Inscription/Desinscription
    path('newRegistration/session/<int:session_id>/',
         views.registration_session,
         name='registrationSession'),
    path('cancelRegistration/session/<int:session_id>/',
         views.cancel_registration_session,
         name='cancelRegistrationSession'),

    # SuppressionFormation et SuppressionSession
    path('formation/<int:formation_id>/delete/',
         views.formation_delete_view.FormationDeleteView.as_view(),
         name='deleteFormation'),
    path('formation/session/<int:sessionFormation_id>/delete/',
         views.session_delete_view.SessionDeleteView.as_view(),
         name='deleteSession'),

    # Calendar
    path('calendar/', views.calendar_view.CalendarView.as_view(), name='calendar'),

    # NavBar
    path('formation/formateur/<int:formateur_id>/',
         views.formation_list_for_formateur_view.FormationListForFormateurView.as_view(),
         name='formation_list_current_formateur'),
    path('formation/student/<int:student_id>/',
         views.registration_list_for_students_view.RegistrationListForStudentsView.as_view(),
         name='inscription_list_current_student'),

    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
    # debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
