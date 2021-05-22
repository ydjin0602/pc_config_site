from marshmallow import Schema, fields, EXCLUDE

from pc_configuration.models.pc_configuration_model import PCConfigurationModel
from pc_configuration.schemas.disk_configuration_shema import DiskConfigurationSchema
from pc_configuration.schemas.os_configuration_schema import OSConfigurationSchema
from pc_configuration.schemas.processor_configuration_schema import ProcessorConfigurationSchema
from pc_configuration.schemas.ram_configuration_schema import RAMConfigurationSchema
from pc_configuration.schemas.socket_configuration_schema import SocketConfigurationSchema


class PCConfigurationSchema(Schema):
    class Meta:
        model = PCConfigurationModel
        unknown = EXCLUDE

    token = fields.Str(dump_only=True)
    os = fields.Nested(OSConfigurationSchema)
    processor = fields.Nested(ProcessorConfigurationSchema)
    socket_info = fields.Nested(SocketConfigurationSchema)
    disk = fields.Nested(DiskConfigurationSchema)
    ram = fields.Nested(RAMConfigurationSchema)
