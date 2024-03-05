from django.db import models

# Create your models here.
class BunchOfKeys(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class DelBunchOfKeys(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    contentDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PutBunchOfKeys(models.Model):
    bunchOfKeysId = models.CharField(max_length=24)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.bunchOfKeysId

class PutKeyNewBunchOfKeys(models.Model):
    keyId = models.CharField(max_length=24)
    bunchOfKeysId = models.CharField(max_length=24)
    newBunchOfKeysId = models.CharField(max_length=24)

    def __str__(self):
        return self.keyId