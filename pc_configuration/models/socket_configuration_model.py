from django.db import models


class SocketConfigurationModel(models.Model):
    host = models.CharField('Socket Info Host', max_length=100, default=None)
    ip_address = models.CharField('Socket Info IP Address', max_length=100, default=None)
    mac_address = models.CharField('Socket Info MAC Address', max_length=100, default=None)
