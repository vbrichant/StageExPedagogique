from django.db import models

from formation.model.SessionFormation import SessionFormation
from formation.model.Student import Student


class Inscription(models.Model):
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.session.formation.name + " " + str(self.session.datetime) + " " + self.student.matricule
