from django.urls import path
from . import views


urlpatterns = [
    path('sign-up/', views.RegisterUserAPI.as_view()),
    path('login/', views.LoginUserAPI.as_view()),
    path('validate-otp/', views.CheckOPTAndReturnJWTTokenAPI.as_view()),
    path('fast-token/', views.FastToken.as_view()),
]
