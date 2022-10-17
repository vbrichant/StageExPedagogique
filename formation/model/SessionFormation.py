from django.db import models
from datetime import datetime

from django.utils import timezone

from formation.model.Formation import Formation


class SessionFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    datetime = models.DateTimeField("date", default=datetime.now())
    place = models.CharField(max_length=200)
    max_students = models.IntegerField()

    def __str__(self):
        return self.formation.name + " " + str(self.datetime)

    def get_count_registration(self):
        return self.inscription_set.count()

    def get_students_registered(self):
        inscription_list = self.inscription_set.values_list("student", flat=True)
        student_list = []
        for inscription in inscription_list:
            student_list.append(int(inscription))
        return inscription_list

    def is_open(self):
        now = timezone.now()
        return self.datetime > now
