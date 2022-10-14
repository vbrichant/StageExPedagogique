from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from formation.model.Inscription import Inscription
from formation.model.SessionFormation import SessionFormation


@login_required
@permission_required('formation.add_inscription', raise_exception=True)
def cancel_registration_session(request, session_id):
    session = get_object_or_404(SessionFormation, pk=session_id)
    student = request.user.student
    inscription = get_object_or_404(Inscription, session=session, student=student)
    inscription.delete()
    return HttpResponseRedirect(reverse('formation:inscription_list_current_student', args=(student.id,)))
