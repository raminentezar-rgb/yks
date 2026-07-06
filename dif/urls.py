from django.urls import path
from . import views

urlpatterns = [
    path('', views.dif_list, name='dif_list'),
]
