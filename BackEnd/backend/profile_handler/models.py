from django.db import models

# Create your models here.

class PutProfileData(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    country_code = models.CharField(max_length=2)
    start_of_day = models.TimeField()
    end_of_day = models.TimeField()
    workdays = models.SmallIntegerField()

    def __str__(self):
        return self.first_name