from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-keyword/', views.add_keyword, name='add_keyword'),
    path('start-recording/', views.start_recording, name='start_recording'),
    path('stop-recording/', views.stop_recording, name='stop_recording'),
    path('recording-status/', views.recording_status, name='recording_status'),
]