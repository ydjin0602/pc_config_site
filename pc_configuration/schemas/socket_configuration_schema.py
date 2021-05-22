from marshmallow import Schema, EXCLUDE, fields

from pc_configuration.models.socket_configuration_model import SocketConfigurationModel


class SocketConfigurationSchema(Schema):
    class Meta:
        model = SocketConfigurationModel
        unknown = EXCLUDE

    host = fields.Str()
    ip_address = fields.Str()
    mac_address = fields.Str()
