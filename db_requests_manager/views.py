import json
import logging
import typing as t
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from marshmallow import ValidationError

from pc_configuration.models import PCConfiguration, PCConfigurationSchema

LOGGER = logging.getLogger(__name__)


@dataclass_json
@dataclass(frozen=True)
class OSConfig:
    name: t.Text
    version: t.Text


@dataclass_json
@dataclass(frozen=True)
class ProcessorConfig:
    name: t.Text
    architecture: t.Text
    temperature: t.Text
    loading: t.Text


@dataclass_json
@dataclass(frozen=True)
class SocketInfoConfig:
    host: t.Text
    ip_address: t.Text
    mac_address: t.Text


@dataclass_json
@dataclass(frozen=True)
class DiskConfig:
    memory: t.Text
    loading: t.Text


@dataclass_json
@dataclass(frozen=True)
class CreateConfigOptions:
    token: t.Text
    os: OSConfig
    processor: ProcessorConfig
    socket_info: SocketInfoConfig
    disk: DiskConfig
    ram: t.Text


@dataclass_json
@dataclass(frozen=True)
class GetConfigOptions:
    token: t.Text


class DBRequestsManagerView(View):
    __GET_PC_CONFIG_SCHEMA = GetConfigOptions.schema()
    __CREATE_PC_CONFIG_SCHEMA = CreateConfigOptions.schema()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DBRequestsManagerView, self).dispatch(request, *args, **kwargs)

    def get(self, request: t.Union[GetConfigOptions, HttpRequest]):

        if isinstance(request, HttpRequest):
            try:
                request_body: GetConfigOptions = self.__GET_PC_CONFIG_SCHEMA.load(request.GET.dict())
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
                return self.__return_bad_request(exception)

            try:
                pc_config = PCConfiguration.objects.get(token=request_body.token)
                pc_config_schema = PCConfigurationSchema().dump(pc_config)
                return JsonResponse(
                    data=pc_config_schema
                )

            except PCConfiguration.DoesNotExist as exception:
                return self.__build_not_found_json_response(f'Configuration (token={request_body.token}) not found.')

        elif isinstance(request, GetConfigOptions):
            try:
                return PCConfiguration.objects.get(token=request.token)
            except PCConfiguration.DoesNotExist as exception:
                raise PCConfiguration.DoesNotExist from exception

    def post(self, request: HttpRequest):
        try:
            request_body = self.__parse_create_config_request(request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__return_bad_request(exception)

    def put(self):
        pass

    def delete(self):
        pass

    def __parse_create_config_request(self, request: HttpRequest) -> CreateConfigOptions:
        return self.__CREATE_PC_CONFIG_SCHEMA.load(json.loads(request.body))

    @staticmethod
    def __build_not_found_json_response(description: str) -> JsonResponse:
        return JsonResponse(
            status=HttpResponseNotFound.status_code,
            data={
                'error': description
            }
        )

    @staticmethod
    def __return_bad_request(exception: t.Any):
        LOGGER.warning('Request body is invalid.', exc_info=exception)
        return JsonResponse(
            status=HttpResponseBadRequest.status_code,
            data={
                'error': 'request body is invalid.'
            }
        )
