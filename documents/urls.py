from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('download/<int:doc_id>/', views.document_download, name='document_download'),
]
