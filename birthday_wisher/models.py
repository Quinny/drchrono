from django.db import models

class Doctor(models.Model):
    access_token = models.CharField(max_length = 100)
    refresh_token = models.CharField(max_length = 100)
    expires = models.DateTimeField()
