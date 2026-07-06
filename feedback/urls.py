from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.feedback_create, name='feedback_create'),
    path('success/<str:tracking_code>/', views.feedback_success, name='feedback_success'),
    path('track/', views.feedback_track, name='feedback_track'),
]
