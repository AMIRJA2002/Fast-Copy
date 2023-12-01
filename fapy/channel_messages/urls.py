from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.CreateChannelAPI.as_view()),
    path('subscribe/', views.SubscriberChannelAPI.as_view()),
]