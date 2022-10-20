from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
