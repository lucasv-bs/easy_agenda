from django.db import models

from users.models import User


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='specialty_creator_set')
    updater = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='specialty_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)