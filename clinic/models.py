from django.db import models


class Clinic(models.Model):
    clinic_oppening = models.TimeField()
    clinic_closing = models.TimeField()
    duration_consultation = models.IntegerField()