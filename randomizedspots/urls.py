from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from listofspots import views
from randomizedspots import views


urlpatterns=[
    path('', views.show_randomized_tools),
    ]


