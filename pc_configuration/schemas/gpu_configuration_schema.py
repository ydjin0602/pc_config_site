from marshmallow import Schema, fields, EXCLUDE

from pc_configuration.models.gpu_configuration_model import GPUConfigurationModel


class GPUConfigurationSchema(Schema):
    class Meta:
        model = GPUConfigurationModel
        unknown = EXCLUDE

    name = fields.Str()
    temperature = fields.Str()
    loading = fields.Str()
    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
