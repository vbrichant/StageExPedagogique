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

    def is_open(self):
        now = timezone.now()
        return self.datetime > now
