from django.db import models


# TODO: add more config info
class PCConfiguration(models.Model):
    token = models.CharField('Token', max_length=100, unique=True)
    os_name = models.CharField('OS Name', max_length=100)
    os_version = models.CharField('OS Version', max_length=100)
    processor_name = models.CharField('Processor Name', max_length=100)
    processor_architecture = models.CharField('Processor Architecture', max_length=100)
    processor_temperature = models.CharField('Processor Temperature', max_length=100)
    processor_loading = models.CharField('Processor Loading', max_length=100)
    socket_info_host = models.CharField('Socket Info Host', max_length=100)
    socket_info_ip_address = models.CharField('Socket Info IP Address', max_length=100)
    socket_info_mac_address = models.CharField('Socket Info MAC Address', max_length=100)
    disk_memory = models.CharField('Disk Memory', max_length=100)
    disk_loading = models.CharField('Disk Loading', max_length=100)
    ram = models.CharField('RAM', max_length=20)
