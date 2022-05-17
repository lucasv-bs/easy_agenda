# django imports
from django.db import models

# project imports
from users.models import User


class Clinic(models.Model):
    clinic_oppening = models.TimeField()
    clinic_closing = models.TimeField()
    consultation_duration = models.IntegerField(default=30)
    days_number_to_search = models.IntegerField(default=7)
    creator = models.ForeignKey(User, default=1 ,on_delete=models.PROTECT, related_name='clinic_creator_set')
    updater = models.ForeignKey(User, default=1 ,on_delete=models.PROTECT, related_name='clinic_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)