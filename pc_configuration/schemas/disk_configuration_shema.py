from marshmallow import Schema, EXCLUDE, fields

from pc_configuration.models.disk_configuration_model import DiskConfigurationModel


class DiskConfigurationSchema(Schema):
    class Meta:
        model = DiskConfigurationModel
        unknown = EXCLUDE

    file_system_type = fields.Str()
    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
