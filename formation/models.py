import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Formateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=50, default=0)

    def __str__(self):
        return self.user.username.replace("_", " ")

    def get_name(self):
        return self.user.username.replace("_", " ")


class Student(models.Model):
    class Meta:
        permissions = [('can_create_inscription', 'can')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.user.username.replace("_", " ")

    def get_name(self):
        return self.user.username.replace("_", " ")


class Formation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SessionFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    date = models.DateTimeField("formation date")
    place = models.CharField(max_length=200)
    max_students = models.IntegerField()

    def __str__(self):
        return self.formation.name + " " + str(self.date)

    def get_count_inscription(self):
        return self.inscription_set.count()

    def is_student_registered(self):
        inscription_list = self.inscription_set.values_list("student", flat=True)
        student_list = []
        for inscription in inscription_list:
            student_list.append(int(inscription))
        return inscription_list

    def is_open(self):
        now = timezone.now()
        today = datetime.datetime.now()
        return self.date > now


class Inscription(models.Model):
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.session.formation.name + " " + str(self.session.date) + " " + self.student.matricule
