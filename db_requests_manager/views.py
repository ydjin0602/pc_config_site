import json
import logging
import typing as t
from http import HTTPStatus

from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from marshmallow import ValidationError, Schema

from db_requests_manager.request_options.delete import DeleteConfigOption
from db_requests_manager.request_options.get import GetConfigOptions
from db_requests_manager.request_options.post import CreateConfigOptions
from db_requests_manager.request_options.put import PutConfigOptions
from pc_configuration.models import PCConfiguration, PCConfigurationSchema

LOGGER = logging.getLogger(__name__)


class DBRequestsManagerView(View):
    __GET_PC_CONFIG_SCHEMA = GetConfigOptions.schema()
    __CREATE_PC_CONFIG_SCHEMA = CreateConfigOptions.schema()
    __PUT_PC_CONFIG_SCHEMA = PutConfigOptions.schema()
    __DELETE_PC_CONFIG_SCHEMA = DeleteConfigOption.schema()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DBRequestsManagerView, self).dispatch(request, *args, **kwargs)

    def get(self, request: t.Union[GetConfigOptions, HttpRequest]) -> HttpResponse:

        if isinstance(request, HttpRequest):
            try:
                request_body: GetConfigOptions = self.__GET_PC_CONFIG_SCHEMA.load(request.GET.dict())
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
                return self.__build_bad_request_response(exception)

            try:
                pc_config = PCConfiguration.objects.get(token=request_body.token)
                pc_config_schema = PCConfigurationSchema().dump(pc_config)
                return JsonResponse(
                    status=HTTPStatus.OK,
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
            request_body: CreateConfigOptions = self.__parse_request(self.__CREATE_PC_CONFIG_SCHEMA, request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__build_bad_request_response(exception)

        try:
            new_config = PCConfiguration.create(request_body)
        except IntegrityError as exception:
            return self.__build_config_already_exist_response(
                f'Configuration (token={request_body.token}) already exist.',
                exception)

        response = PCConfigurationSchema().dump(new_config)

        return JsonResponse(
            status=HTTPStatus.CREATED,
            data=response
        )

    def put(self, request) -> HttpResponse:
        try:
            request_body: PutConfigOptions = self.__parse_request(self.__PUT_PC_CONFIG_SCHEMA, request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__build_bad_request_response(exception)

        try:
            pc_config = PCConfiguration.objects.get(token=request_body.token)
        except PCConfiguration.DoesNotExist as exception:
            return self.__build_not_found_json_response(f'Configuration (token={request_body.token}) not found.',
                                                        exception)

        pc_config.update(request_body)
        response = PCConfigurationSchema().dump(pc_config)

        return JsonResponse(
            status=HTTPStatus.OK,
            data=response
        )

    def delete(self, request: HttpRequest) -> HttpResponse:
        try:
            request_body: DeleteConfigOption = self.__parse_request(self.__DELETE_PC_CONFIG_SCHEMA, request)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__build_bad_request_response(exception)

        try:
            pc_config = PCConfiguration.objects.get(token=request_body.token)
        except PCConfiguration.DoesNotExist as exception:
            return self.__build_not_found_json_response(f'Configuration (token={request_body.token}) not found.',
                                                        exception)
        pc_config.delete()
        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'result': f'Configuration (token={request_body.token}) successfully deleted.'
            }
        )

    @staticmethod
    def __parse_request(schema: Schema, request: HttpRequest) -> t.Union[
        CreateConfigOptions, DeleteConfigOption, PutConfigOptions
    ]:
        return schema.load(json.loads(request.body))

    @staticmethod
    def __build_not_found_json_response(description: str, exception: t.Any) -> JsonResponse:
        LOGGER.warning(description, exc_info=exception)
        return JsonResponse(
            status=HTTPStatus.NOT_FOUND,
            data={
                'error': description
            }
        )

    @staticmethod
    def __build_config_already_exist_response(description: str, exception: t.Any) -> JsonResponse:
        LOGGER.warning(description, exc_info=exception)
        return JsonResponse(
            status=HTTPStatus.CONFLICT,
            data={
                'error': description
            }
        )

    @staticmethod
    def __build_bad_request_response(exception: t.Any) -> JsonResponse:
        LOGGER.warning('Request body is invalid.', exc_info=exception)
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={
                'error': 'Request body is invalid.'
            }
        )
