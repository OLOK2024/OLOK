from django.db import models

# Create your models here.
class Key(models.Model):
    domain = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.domain

class InfoKey(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    keyId = models.CharField(max_length=24)

    def __str__(self):
        return self.bunchOfKeysId

class AddKey(models.Model):
    domain = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    bunchOfKeysId = models.CharField(max_length=24)

    def __str__(self):
        return self.domain

class PutKeyUsername(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    keyId = models.CharField(max_length=24)
    newUsername = models.CharField(max_length=255)

    def __str__(self):
        return self.bunchOfKeysId

class PutKeyPassword(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    keyId = models.CharField(max_length=24)
    newPassword = models.CharField(max_length=255)

    def __str__(self):
        return self.bunchOfKeysId

class PutKeyDomain(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    keyId = models.CharField(max_length=24)
    newDomain = models.CharField(max_length=255)

    def __str__(self):
        return self.bunchOfKeysId