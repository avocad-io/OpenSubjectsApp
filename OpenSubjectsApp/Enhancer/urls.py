from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("downloadjson/", views.downloadjson, name="downloadjson"),
    path("downloadcsv/", views.downloadcsv, name="downloadcsv")

]