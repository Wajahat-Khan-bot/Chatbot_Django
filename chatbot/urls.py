from django.urls import path
from .views import ChatResponse, index


urlpatterns = [
    path('chat/<slug:identifier>/', index, name = 'page'),
    path('chat_response/', ChatResponse.as_view(), name = 'chat_response'),
]
