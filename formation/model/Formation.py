from django.db import models

from formation.model.Formateur import Formateur


class Formation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
