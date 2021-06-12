from django.db import models


class GPUConfigurationModel(models.Model):
    name = models.CharField('GPU Name', max_length=100)
    temperature = models.CharField('GPU Temperature', max_length=100, default=None)
    loading = models.CharField('GPU Loading', max_length=100, default=None)
    total_memory = models.CharField('Total GPU Memory', max_length=100, default=None)
    available = models.CharField('Available GPU Memory', max_length=100, default=None)
    used = models.CharField('Used GPU Memory', max_length=100, default=None)
    used_in_percents = models.CharField('Used GPU Memory In Percents', max_length=100, default=None)
