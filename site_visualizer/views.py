import json
import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from marshmallow import ValidationError

from db_requests_manager.views import DBRequestsManagerView, GetConfigOptions
from pc_configuration.models.pc_configuration_model import PCConfigurationModel

LOGGER = logging.getLogger(__name__)


class PageVisualizerView(View):
    __REQUEST_BODY_SCHEMA = GetConfigOptions.schema()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PageVisualizerView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        # TODO: update index.html
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            request_body = self.__parse_interview(request.POST.dict())
            pc_config = DBRequestsManagerView().get(request_body)
            # TODO: update pc_config.html
            return render(request, 'pc_config.html', {'pc_config': pc_config})

        except (
                PCConfigurationModel.DoesNotExist, json.JSONDecodeError, KeyError, UnicodeDecodeError,
                ValidationError) as exception:
            # TODO: update error.html
            LOGGER.warning('Invalid token error', exc_info=exception)
            return render(request, 'error.html')

    def __parse_interview(self, request: HttpRequest) -> GetConfigOptions:
        return self.__REQUEST_BODY_SCHEMA.load(request)
