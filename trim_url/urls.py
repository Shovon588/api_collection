from django.urls import path

from .views import TrimLink, ClickInfoView, handle_short_url

urlpatterns = [
    path('', TrimLink.as_view(), name="trim_link"),
    path('<str:hashed_code>/', handle_short_url, name="handle_short_url"),
    path('click-info/<str:hashed_code>/', ClickInfoView.as_view(), name="click-info"),
]
