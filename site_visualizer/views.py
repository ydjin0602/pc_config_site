from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from pc_configuration.models import PCConfiguration


class PageVisualizer(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PageVisualizer, self).dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        # TODO: update index.html
        return render(request, 'index.html')

    def post(self, request):
        try:
            pc_config = PCConfiguration.objects.get(token=request.POST['token'])
            # TODO: update pc_config.html
            return render(request, 'pc_config.html', {'pc_config': pc_config})

        except PCConfiguration.DoesNotExist:
            # TODO: update error.html
            return render(request, 'error.html')
