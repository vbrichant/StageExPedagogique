from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


@login_required
@permission_required('formation.add_inscription', raise_exception=True)
def registration_session(request, session_id):
    session = get_object_or_404(SessionFormation, pk=session_id)
    user = request.user
    if session.get_count_registration() < session.max_students:
        new_inscription = Inscription(session=session, student=user.student)
        new_inscription.save()
        return HttpResponseRedirect(reverse('formation:inscription_list_current_student', args=(user.student.id,)))
    else:
        messages.error(request, "Le nombre d'inscription maximum est déjà atteint, Choisissez une autre session.")
        return HttpResponseRedirect(reverse('formation:formation_detail', args=(session.formation.id,)))

