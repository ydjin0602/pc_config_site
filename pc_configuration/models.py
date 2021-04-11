from django.db import models
from marshmallow import Schema, fields

from db_requests_manager.request_options.post import CreateConfigOptions
from db_requests_manager.request_options.put import PutConfigOptions


class OSConfiguration(models.Model):
    name = models.CharField('OS Name', max_length=100, default=None)
    version = models.CharField('OS Version', max_length=100, default=None)


class ProcessorConfiguration(models.Model):
    name = models.CharField('Processor Name', max_length=100)
    architecture = models.CharField('Processor Architecture', max_length=100, default=None)
    temperature = models.CharField('Processor Temperature', max_length=100, default=None)
    loading = models.CharField('Processor Loading', max_length=100, default=None)


class SocketConfiguration(models.Model):
    host = models.CharField('Socket Info Host', max_length=100, default=None)
    ip_address = models.CharField('Socket Info IP Address', max_length=100, default=None)
    mac_address = models.CharField('Socket Info MAC Address', max_length=100, default=None)


class DiskConfiguration(models.Model):
    memory = models.CharField('Disk Memory', max_length=100, default=None)
    loading = models.CharField('Disk Loading', max_length=100, default=None)


# TODO: add more config info
class PCConfiguration(models.Model):
    token = models.CharField('Token', max_length=100, unique=True)
    os = models.ForeignKey(OSConfiguration, on_delete=models.CASCADE)
    processor = models.ForeignKey(ProcessorConfiguration, on_delete=models.CASCADE)
    socket_info = models.ForeignKey(SocketConfiguration, on_delete=models.CASCADE)
    disk = models.ForeignKey(DiskConfiguration, on_delete=models.CASCADE)
    ram = models.CharField('RAM', max_length=20, default=None)

    @classmethod
    def create(cls, options: CreateConfigOptions) -> 'PCConfiguration':
        os_config = OSConfiguration(
            name=options.os.name,
            version=options.os.version
        )
        processor_config = ProcessorConfiguration(
            name=options.processor.name,
            architecture=options.processor.architecture,
            temperature=options.processor.temperature,
            loading=options.processor.loading,
        )

        socket_config = SocketConfiguration(
            host=options.socket_info.host,
            ip_address=options.socket_info.ip_address,
            mac_address=options.socket_info.mac_address,
        )

        disk_config = DiskConfiguration(
            memory=options.disk.memory,
            loading=options.disk.loading,
        )

        os_config.save()
        processor_config.save()
        socket_config.save()
        disk_config.save()

        new_config = cls.objects.create(
            token=options.token,
            os=os_config,
            processor=processor_config,
            socket_info=socket_config,
            disk=disk_config,
            ram=options.ram
        )

        new_config.save()

        return new_config

    def update(self, options: PutConfigOptions):

        if options.os:
            self.os.name = options.os.name if options.os.name else self.os.name
            self.os.version = options.os.version if options.os.version else self.os.version
            self.os.save()

        if options.processor:
            self.processor.name = options.processor.name if options.processor.name else self.processor.name
            self.processor.architecture = options.processor.architecture if options.processor.architecture \
                else self.processor.architecture
            self.processor.temperature = options.processor.temperature if options.processor.temperature \
                else self.processor.temperature
            self.processor.loading = options.processor.loading if options.processor.loading else self.processor.loading

            self.processor.save()

        if options.socket_info:
            self.socket_info.host = options.socket_info.host if options.socket_info.host else self.socket_info.host
            self.socket_info.ip_address = options.socket_info.ip_address if options.socket_info.ip_address \
                else self.socket_info.ip_address
            self.socket_info.mac_address = options.socket_info.mac_address if options.socket_info.mac_address \
                else self.socket_info.mac_address

            self.socket_info.save()

        if options.disk:
            self.disk.memory = options.disk.memory if options.disk.memory else self.disk.memory
            self.disk.loading = options.disk.loading if options.disk.loading else self.disk.loading

            self.disk.save()

        self.save()
        return self


class OSConfigurationSchema(Schema):
    name = fields.Str()
    version = fields.Str()


class ProcessorConfigurationSchema(Schema):
    name = fields.Str()
    architecture = fields.Str()
    temperature = fields.Str()
    loading = fields.Str()


class SocketConfigurationSchema(Schema):
    host = fields.Str()
    ip_address = fields.Str()
    mac_address = fields.Str()


class DiskConfigurationSchema(Schema):
    memory = fields.Str()
    loading = fields.Str()


class PCConfigurationSchema(Schema):
    token = fields.Str(dump_only=True)
    os = fields.Nested(OSConfigurationSchema)
    processor = fields.Nested(ProcessorConfigurationSchema)
    socket_info = fields.Nested(SocketConfigurationSchema)
    disk = fields.Nested(DiskConfigurationSchema)
    ram = fields.Str()
