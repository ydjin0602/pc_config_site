from marshmallow import Schema, EXCLUDE, fields

from pc_configuration.models.processor_configuration_model import ProcessorConfigurationModel


class ProcessorConfigurationSchema(Schema):
    class Meta:
        model = ProcessorConfigurationModel
        unknown = EXCLUDE

    name = fields.Str()
    architecture = fields.Str()
    total_cores = fields.Int()
    max_frequency = fields.Str()
    current_frequency = fields.Str()
    temperature = fields.Str()
    loading = fields.Str()
    usage_per_core = fields.Str()
