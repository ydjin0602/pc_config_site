from django.contrib import admin
from django.urls import path

from site_visualizer.views import PageVisualizer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PageVisualizer.as_view(), name=''),
]
