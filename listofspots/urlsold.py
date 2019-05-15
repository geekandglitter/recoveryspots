from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from listofspots import views


urlpatterns = [
    path('getpostcontents', views.getpostcontents),
    path('puttoolsinamodel', views.puttoolsinamodel),
    path('show_the_model_data', views.show_the_model_data),
    path('bulkstoretoolsinamodel', views.bulkstoretoolsinamodel),
    path('show_the_model_data_bulk_stored', views.show_the_model_data_bulk_stored),
    ]
