from django.urls import path

from . import views

urlpatterns = [
    path('', views.enhancer_query_bn, name='enhancer_query_bn'),
    path("downloadjson/", views.downloadjson, name="downloadjson"),
    path("downloadcsv/", views.downloadcsv, name="downloadcsv")

]