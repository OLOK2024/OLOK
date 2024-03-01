from django.db import models

# Create your models here.
class Key(models.Model):
    domain = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.domain