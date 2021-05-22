from django.db import models

from db_requests_manager.request_options.post import PostConfigOptions
from db_requests_manager.request_options.put import PutConfigOptions
from pc_configuration.models.os_configuration_model import OSConfigurationModel

from pc_configuration.models.processor_configuration_model import ProcessorConfigurationModel

from pc_configuration.models.socket_configuration_model import SocketConfigurationModel

from pc_configuration.models.disk_configuration_model import DiskConfigurationModel

from pc_configuration.models.ram_configuration_model import RAMConfigurationModel


class PCConfigurationModel(models.Model):
    token = models.CharField('Token', max_length=100, unique=True)
    os = models.ForeignKey(OSConfigurationModel, on_delete=models.CASCADE)
    processor = models.ForeignKey(ProcessorConfigurationModel, on_delete=models.CASCADE)
    socket_info = models.ForeignKey(SocketConfigurationModel, on_delete=models.CASCADE)
    disk = models.ForeignKey(DiskConfigurationModel, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAMConfigurationModel, on_delete=models.CASCADE)

    @classmethod
    def create(cls, options: PostConfigOptions) -> 'PCConfigurationModel':
        os_config = OSConfigurationModel(
            name=options.os.name,
            version=options.os.version,
        )
        processor_config = ProcessorConfigurationModel(
            name=options.processor.name,
            architecture=options.processor.architecture,
            total_cores=options.processor.total_cores,
            max_frequency=options.processor.max_frequency,
            current_frequency=options.processor.current_frequency,
            temperature=options.processor.temperature,
            loading=options.processor.loading,
            usage_per_core=options.processor.usage_per_core,
        )

        socket_config = SocketConfigurationModel(
            host=options.socket_info.host,
            ip_address=options.socket_info.ip_address,
            mac_address=options.socket_info.mac_address,
        )

        disk_config = DiskConfigurationModel(
            file_system_type=options.disk.file_system_type,
            total_memory=options.disk.total_memory,
            available=options.disk.available,
            used=options.disk.used,
            used_in_percents=options.disk.used_in_percents,
        )

        ram_config = RAMConfigurationModel(
            total_memory=options.ram.total_memory,
            available=options.ram.available,
            used=options.ram.used,
            used_in_percents=options.ram.used_in_percents,
        )

        os_config.save()
        processor_config.save()
        socket_config.save()
        disk_config.save()
        ram_config.save()

        new_config = cls.objects.create(
            token=options.token,
            os=os_config,
            processor=processor_config,
            socket_info=socket_config,
            disk=disk_config,
            ram=ram_config,
        )

        new_config.save()

        return new_config

    def update(self, options: PutConfigOptions) -> 'PCConfigurationModel':

        if options.os:
            self.os.name = options.os.name if options.os.name else self.os.name
            self.os.version = options.os.version if options.os.version else self.os.version
            self.os.save()

        if options.processor:
            self.processor.name = options.processor.name if options.processor.name else self.processor.name
            self.processor.architecture = options.processor.architecture if options.processor.architecture \
                else self.processor.architecture
            self.processor.total_cores = options.processor.total_cores if options.processor.total_cores \
                else self.processor.total_cores
            self.processor.max_frequency = options.processor.max_frequency if options.processor.max_frequency \
                else self.processor.max_frequency
            self.processor.current_frequency = options.processor.current_frequency if \
                options.processor.current_frequency else self.processor.current_frequency
            self.processor.temperature = options.processor.temperature if options.processor.temperature \
                else self.processor.temperature
            self.processor.loading = options.processor.loading if options.processor.loading else self.processor.loading
            self.processor.usage_per_core = options.processor.usage_per_core if options.processor.usage_per_core \
                else self.processor.usage_per_core

            self.processor.save()

        if options.socket_info:
            self.socket_info.host = options.socket_info.host if options.socket_info.host else self.socket_info.host
            self.socket_info.ip_address = options.socket_info.ip_address if options.socket_info.ip_address \
                else self.socket_info.ip_address
            self.socket_info.mac_address = options.socket_info.mac_address if options.socket_info.mac_address \
                else self.socket_info.mac_address

            self.socket_info.save()

        if options.disk:
            self.disk.file_system_type = options.disk.file_system_type if options.disk.file_system_type \
                else self.disk.file_system_type
            self.disk.total_memory = options.disk.total_memory if options.disk.total_memory else self.disk.total_memory
            self.disk.available = options.disk.available if options.disk.available else self.disk.available
            self.disk.used = options.disk.used if options.disk.used else self.disk.used
            self.disk.used_in_percents = options.disk.used_in_percents if options.disk.used_in_percents \
                else self.disk.used_in_percents

            self.disk.save()

        if options.ram:
            self.ram.total_memory = options.ram.total_memory if options.ram.total_memory else self.ram.total_memory
            self.ram.available = options.ram.available if options.ram.available else self.ram.available
            self.ram.used = options.ram.used if options.ram.used else self.ram.used
            self.ram.used_in_percents = options.ram.used_in_percents if options.ram.used_in_percents \
                else self.ram.used_in_percents
            self.ram.save()
        self.save()
        return self
