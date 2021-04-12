from http import HTTPStatus
from uuid import uuid4

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class TokenGeneratorView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(TokenGeneratorView, self).dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        token = uuid4()
        return JsonResponse(
            status=HTTPStatus.OK,
            data={
                'token': token
            }
        )
