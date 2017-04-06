from django.conf.urls import url
from django.contrib import admin

from productos import views
from productos.views import (ProductoListView,
                             ProductoDetailView,
                             ProductoCreateView,
                             ProductoUpdateView,
                             ProductoDownloadView)

urlpatterns = [
    url(r'^lista/$', ProductoListView.as_view(), name='lista'),
    url(r'^crear/$', ProductoCreateView.as_view(), name='crear'),
    url(r'^(?P<pk>\d+)/$', ProductoDetailView.as_view(), name='detalle'),
    url(r'^(?P<slug>[\w-]+)/$', ProductoDetailView.as_view(), name='detalle_slug'),
    url(r'^(?P<pk>\d+)/download/$', ProductoDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductoDownloadView.as_view(), name='download_slug'),
    url(r'^(?P<pk>\d+)/editar/$', ProductoUpdateView.as_view(), name='actualizar'),
]
