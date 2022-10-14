from django.contrib.auth.models import User
from django.db import models


class Formateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=50, default=0)

    def __str__(self):
        return self.user.username.replace("_", " ")

    def get_name(self):
        return self.user.username.replace("_", " ")