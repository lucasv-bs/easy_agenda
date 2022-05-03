from django.db import models

from users.models import User


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='specialty_creator_set')
    updater = models.ForeignKey(User, on_delete=models.PROTECT, related_name='specialty_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name