from django.db import models


class OSConfigurationModel(models.Model):
    name = models.CharField('OS Name', max_length=100, default=None)
    version = models.CharField('OS Version', max_length=100, default=None)
