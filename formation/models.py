from datetime import datetime

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
    date = models.DateField("date")
    time = models.TimeField("time")
    place = models.CharField(max_length=200)
    max_students = models.IntegerField()

    def __str__(self):
        return self.formation.name + " " + str(self.get_date_time())

    def get_count_registration(self):
        return self.inscription_set.count()

    def get_students_registered(self):
        inscription_list = self.inscription_set.values_list("student", flat=True)
        student_list = []
        for inscription in inscription_list:
            student_list.append(int(inscription))
        return inscription_list

    def get_date_time(self):
        return datetime.combine(date=self.date, time=self.time)

    def is_open(self):
        now = datetime.now()
        return self.get_date_time() > now


class Inscription(models.Model):
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.session.formation.name + " " + str(self.session.date) + " " + self.student.matricule
