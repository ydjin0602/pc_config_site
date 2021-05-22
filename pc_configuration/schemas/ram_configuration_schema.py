from marshmallow import Schema, EXCLUDE, fields

from pc_configuration.models.ram_configuration_model import RAMConfigurationModel


class RAMConfigurationSchema(Schema):
    class Meta:
        model = RAMConfigurationModel
        unknown = EXCLUDE

    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
