from django.contrib import admin
from django.urls import path

from db_requests_manager.views import DBRequestsManagerView
from site_visualizer.views import PageVisualizerView
from token_generator.views import TokenGeneratorView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PageVisualizerView.as_view(), name=''),
    path('db_manager/', DBRequestsManagerView.as_view(), name='db_manager'),
    path('token_generator/', TokenGeneratorView.as_view(), name='token_generator'),
]
