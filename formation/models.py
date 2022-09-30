from django.db import models


# Create your models here.
class Formateur(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __str__(self):
        return self.firstname + " " + self.lastname


class Student(models.Model):
    matricule = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __str__(self):
        return self.matricule


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


class Inscription(models.Model):
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.session.formation.name + " " + str(self.session.date) + " " + self.student.matricule
