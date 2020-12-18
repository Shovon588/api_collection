from django.urls import path

from .views import YoutubeDL

urlpatterns = [
    path('', YoutubeDL.as_view(), name="trim_link"),
]
