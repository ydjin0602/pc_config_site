from django.db import models


class DiskConfigurationModel(models.Model):
    file_system_type = models.CharField('File System Type', max_length=100, default=None)
    total_memory = models.CharField('Total Disk Memory', max_length=100, default=None)
    available = models.CharField('Available Disk Memory', max_length=100, default=None)
    used = models.CharField('Used Disk Memory', max_length=100, default=None)
    used_in_percents = models.CharField('Used Disk Memory In Percents', max_length=100, default=None)
