from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse

from .models import *


def create_user(user_name):
    return User.objects.create_user(username=user_name)


def create_student(student_name):
    return Student.objects.create(user=create_user(user_name=student_name))


def create_formateur(formateur_name):
    return Formateur.objects.create(user=create_user(user_name=formateur_name))


def create_formation(name, formateur):
    return Formation.objects.create(name=name, formateur=formateur)


def create_session_formation(formation: Formation, date: datetime, place: str, max_students: int):
    return SessionFormation.objects.create(formation=formation,
                                           date=date.date(),
                                           time=date.time(),
                                           place=place,
                                           max_students=max_students)

    # Create your tests here.


class SessionFormationModelTest(TestCase):
    # Test is_close()
    def test_is_close_with_future_session(self):
        date = datetime.now() + timedelta(days=30)
        future_session = SessionFormation(date=date.date(), time=date.time())
        self.assertIs(future_session.is_open(), True)

    def test_is_close_with_past_session(self):
        date = datetime.now() - timedelta(days=30)
        future_session = SessionFormation(date=date.date(), time=date.time())
        self.assertIs(future_session.is_open(), False)

    def test_is_close_with_today_but_future_session(self):
        date = datetime.now() + timedelta(minutes=15)
        future_session = SessionFormation(date=date.date(), time=date.time())
        self.assertIs(future_session.is_open(), True)

    def test_is_close_with_today_but_past_session(self):
        date = datetime.now() - timedelta(minutes=15)
        future_session = SessionFormation(date=date.date(), time=date.time())
        self.assertIs(future_session.is_open(), False)


class FormationListForFormateurViewTest(TestCase):

    def test_without_formation(self):
        response = self.client.get(reverse('formation:formation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune formation n'est disponible")
        self.assertQuerysetEqual(response.context['formation_list'], [])

    def test_with_one_formation(self):
        formateur = create_formateur(formateur_name="formateur_test")
        formation = create_formation(formateur=formateur, name="formation_test")
        response = self.client.get(reverse('formation:formation_list'))
        self.assertQuerysetEqual(
            response.context['formation_list'],
            [formation],
        )

    def test_with_two_formation(self):
        formateur = create_formateur(formateur_name="formateur_test")
        formation1 = create_formation(formateur=formateur, name="formation_test_1")
        formation2 = create_formation(formateur=formateur, name="formation_test_2")
        response = self.client.get(reverse('formation:formation_list'))
        self.assertQuerysetEqual(
            response.context['formation_list'],
            [formation2, formation1],
            ordered=False,
        )


class FormationListForFormateurView(TestCase):
    def test_without_formation(self):
        formateur1 = create_formateur(formateur_name="formateur_test")
        url = reverse('formation:formation_list_current_formateur', args=[formateur1.user.formateur.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # self.assertContains(response, "Aucune formation n'est disponible")
        # self.assertQuerysetEqual(response.context['formation_list'], [])

    def test_with_one_formation_created_by_formateur(self):
        pass

    def test_with_one_formation_not_created_by_formateur(self):
        pass

    def test_with_two_formation_but_one_created_by_formateur(self):
        pass


class RegistrationListForStudentsView(TestCase):
    pass
