from django.contrib import admin
from django.urls import path
from .views import Thing_list,Thing_detail

urlpatterns = [
    path('',Thing_list.as_view(), name='Thing_list' ),
    path('<int:pk>',Thing_detail.as_view(),name='Thing_detail' ),
]
