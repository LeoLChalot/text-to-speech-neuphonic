from django.urls import path
from . import views

urlpatterns = [
    path('', views.neutts_view, name='neutts'),
    path('serve-audio/', views.serve_audio_view, name='serve_audio'),
    path('audio/<str:filename>/', views.serve_audio_view, name='serve_audio_filename'),
    path('api/generate/', views.api_generate_view, name='api_generate'),
]
