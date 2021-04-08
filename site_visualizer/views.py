import json
import logging
import typing as t
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from marshmallow import ValidationError

from pc_configuration.models import PCConfiguration

LOGGER = logging.getLogger(__name__)


@dataclass_json
@dataclass(frozen=True)
class GetConfigOption:
    token: t.Text


class PageVisualizer(View):
    __REQUEST_BODY_SCHEMA = GetConfigOption.schema()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PageVisualizer, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request: HttpRequest):
        # TODO: update index.html
        return render(request, 'index.html')

    def post(self, request):
        try:
            request_body = self.__parse_interview(request.POST.dict())
            pc_config = PCConfiguration.objects.get(token=request_body.token)
            # TODO: update pc_config.html
            return render(request, 'pc_config.html', {'pc_config': pc_config})

        except (
                PCConfiguration.DoesNotExist, json.JSONDecodeError, KeyError, UnicodeDecodeError,
                ValidationError) as exception:
            # TODO: update error.html
            LOGGER.warning('Invalid token error', exc_info=exception)
            return render(request, 'error.html')

    def __parse_interview(self, request: HttpRequest) -> GetConfigOption:
        return self.__REQUEST_BODY_SCHEMA.load(request)
