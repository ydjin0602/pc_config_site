import json
import logging
import typing as t
from dataclasses import dataclass
from http import HTTPStatus

from dataclasses_json import dataclass_json
from django.db import IntegrityError
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


@dataclass_json
@dataclass(frozen=True)
class DeleteConfigOption:
    token: t.Text


class DBRequestsManagerView(View):
    __GET_PC_CONFIG_SCHEMA = GetConfigOptions.schema()
    __CREATE_PC_CONFIG_SCHEMA = CreateConfigOptions.schema()
    __DELETE_PC_CONFIG_SCHEMA = DeleteConfigOption.schema()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DBRequestsManagerView, self).dispatch(request, *args, **kwargs)

    def get(self, request: t.Union[GetConfigOptions, HttpRequest]) -> HttpResponse:

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
                return self.__build_not_found_json_response(f'Configuration (token={request_body.token}) not found.',
                                                            exception)

        elif isinstance(request, GetConfigOptions):
            try:
                return PCConfiguration.objects.get(token=request.token)
            except PCConfiguration.DoesNotExist as exception:
                raise PCConfiguration.DoesNotExist from exception

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            request_body = self.__parse_create_config_request(request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__return_bad_request(exception)

        try:

            new_config = PCConfiguration(
                token=request_body.token,
                os_name=request_body.os.name,
                os_version=request_body.os.version,
                processor_name=request_body.processor.name,
                processor_loading=request_body.processor.loading,
                processor_architecture=request_body.processor.architecture,
                processor_temperature=request_body.processor.temperature,
                socket_info_host=request_body.socket_info.host,
                socket_info_ip_address=request_body.socket_info.ip_address,
                socket_info_mac_address=request_body.socket_info.mac_address,
                disk_loading=request_body.disk.loading,
                disk_memory=request_body.disk.memory,
                ram=request_body.ram
            )
            new_config.save()
        except IntegrityError as exception:
            return self.__build_config_already_exist(f'Configuration (token={request_body.token}) already exist.',
                                                     exception)

        config = PCConfigurationSchema().dump(new_config)

        return JsonResponse(
            status=HTTPStatus.CREATED,
            data=config
        )

    def put(self) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        try:
            request_body = self.__parse_delete_config_request(request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__return_bad_request(exception)

        try:
            pc_config = PCConfiguration.objects.get(token=request_body.token)
        except PCConfiguration.DoesNotExist as exception:
            return self.__build_not_found_json_response(f'Configuration (token={request_body.token}) not found.',
                                                        exception)
        pc_config.delete()
        return JsonResponse(
            {
                'result': f'Configuration (token={request_body.token}) successfully deleted.'
            }
        )

    def __parse_create_config_request(self, request: HttpRequest) -> CreateConfigOptions:
        return self.__CREATE_PC_CONFIG_SCHEMA.load(json.loads(request.body))

    def __parse_delete_config_request(self, request: HttpRequest) -> DeleteConfigOption:
        return self.__DELETE_PC_CONFIG_SCHEMA.load(json.loads(request.body))

    @staticmethod
    def __build_not_found_json_response(description: str, exception: t.Any) -> JsonResponse:
        LOGGER.warning(description, exc_info=exception)
        return JsonResponse(
            status=HttpResponseNotFound.status_code,
            data={
                'error': description
            }
        )

    @staticmethod
    def __build_config_already_exist(description: str, exception: t.Any) -> JsonResponse:
        LOGGER.warning(description, exc_info=exception)
        return JsonResponse(
            status=HTTPStatus.CONFLICT,
            data={
                'error': description
            }
        )

    @staticmethod
    def __return_bad_request(exception: t.Any) -> JsonResponse:
        LOGGER.warning('Request body is invalid.', exc_info=exception)
        return JsonResponse(
            status=HttpResponseBadRequest.status_code,
            data={
                'error': 'request body is invalid.'
            }
        )
