from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('announcements/', views.announcement_list_view, name='announcement_list'),
    path('announcements/<int:pk>/', views.announcement_detail_view, name='announcement_detail'),
]
