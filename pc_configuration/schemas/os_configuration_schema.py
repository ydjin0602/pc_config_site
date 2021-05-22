from marshmallow import Schema, EXCLUDE, fields

from pc_configuration.models.os_configuration_model import OSConfigurationModel


class OSConfigurationSchema(Schema):
    class Meta:
        model = OSConfigurationModel
        unknown = EXCLUDE

    name = fields.Str()
    version = fields.Str()
