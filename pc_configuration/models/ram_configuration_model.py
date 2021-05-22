from django.db import models


class RAMConfigurationModel(models.Model):
    total_memory = models.CharField('Total RAM Memory', max_length=100, default=None)
    available = models.CharField('Available RAM Memory', max_length=100, default=None)
    used = models.CharField('Used RAM Memory', max_length=100, default=None)
    used_in_percents = models.CharField('Used RAM Memory In Percents', max_length=100, default=None)
