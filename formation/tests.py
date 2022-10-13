from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse

from .models import *


def create_user(user_name):
    return User.objects.create_user(username=user_name)


def create_student(student_name, matricule):
    return Student.objects.create(user=create_user(user_name=student_name), matricule=matricule)


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


def create_registration(session: SessionFormation, student: Student):
    return Inscription.objects.create(session=session, student=student)
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


class FormationListViewTest(TestCase):

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


class FormationListForFormateurViewTest(TestCase):

    def test_without_formation(self):
        formateur1 = create_formateur(formateur_name="formateur_test1")
        self.client.force_login(User.objects.get_or_create(username='formateur_test1')[0])
        url = reverse('formation:formation_list_current_formateur', args=[formateur1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune formation n'est disponible")
        self.assertQuerysetEqual(response.context['formation_list'], [])

    def test_with_one_formation_created_by_formateur(self):
        formateur1 = create_formateur(formateur_name="formateur_test1")
        formation1 = create_formation(formateur=formateur1, name="formation_test_1")
        self.client.force_login(User.objects.get_or_create(username='formateur_test1')[0])
        url = reverse('formation:formation_list_current_formateur', args=[formateur1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertQuerysetEqual(response.context['formation_list'], [formation1], ordered=False)

    def test_with_one_formation_not_created_by_formateur(self):
        formateur1 = create_formateur(formateur_name="formateur_test1")
        formateur2 = create_formateur(formateur_name="formateur_test2")
        formation1 = create_formation(formateur=formateur2, name="formation_test_1")
        self.client.force_login(User.objects.get_or_create(username='formateur_test1')[0])
        url = reverse('formation:formation_list_current_formateur', args=[formateur1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune formation n'est disponible")
        self.assertQuerysetEqual(response.context['formation_list'], [], ordered=False)

    def test_with_two_formation_but_one_created_by_formateur(self):
        formateur1 = create_formateur(formateur_name="formateur_test1")
        formateur2 = create_formateur(formateur_name="formateur_test2")
        formation1 = create_formation(formateur=formateur1, name="formation_test_1")
        formation2 = create_formation(formateur=formateur2, name="formation_test_2")
        self.client.force_login(User.objects.get_or_create(username='formateur_test1')[0])
        url = reverse('formation:formation_list_current_formateur', args=[formateur1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertQuerysetEqual(response.context['formation_list'], [formation1], ordered=False)


class RegistrationListForStudentsViewTest(TestCase):
    def test_without_registration(self):
        date = datetime.now()
        student1 = create_student(student_name="student_test_1",matricule='HE200000')
        formateur1 = create_formateur(formateur_name="formateur_test_1")
        formation1 = create_formation(formateur=formateur1, name="formation_test_1")
        session1 = create_session_formation(formation=formation1, date=date, place='test', max_students=15)
        self.client.force_login(User.objects.get_or_create(username='student_test_1')[0])
        url = reverse('formation:inscription_list_current_student', args=[student1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune inscription disponible")
        self.assertQuerysetEqual(response.context['registration_list'], [])

    def test_with_one_registration_for_student(self):
        date = datetime.now()
        student1 = create_student(student_name="student_test_1",matricule="HE200000")
        formateur1 = create_formateur(formateur_name="formateur_test_1")
        formation1 = create_formation(formateur=formateur1, name="formation_test_1")
        session1 = create_session_formation(formation=formation1, date=date, place='test', max_students=15)
        registration1 = create_registration(session=session1, student=student1)
        self.client.force_login(User.objects.get_or_create(username='student_test_1')[0])
        url = reverse('formation:inscription_list_current_student', args=[student1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, registration1.session.formation)
        self.assertQuerysetEqual(response.context['registration_list'], [registration1])
