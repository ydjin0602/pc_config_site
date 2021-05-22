from django.db import models


class ProcessorConfigurationModel(models.Model):
    name = models.CharField('Processor Name', max_length=100)
    architecture = models.CharField('Processor Architecture', max_length=100, default=None)
    total_cores = models.IntegerField('Total Cores', default=None)
    max_frequency = models.CharField('Max Frequency', max_length=100, default=None)
    current_frequency = models.CharField('Current Frequency', max_length=100, default=None)
    temperature = models.CharField('Processor Temperature', max_length=100, default=None)
    loading = models.CharField('Processor Loading', max_length=100, default=None)
    usage_per_core = models.CharField('Usage Per Core', max_length=1000, default=None)
