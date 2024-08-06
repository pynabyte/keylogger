from user_management.views import LoginView,RegisterView,ProfileView,GoogleLoginApi
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("login",LoginView.as_view(),name="login"),
    path("profile",ProfileView.as_view(),name="profile"),
    path("register",RegisterView.as_view(),name="register"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('google', GoogleLoginApi.as_view(), name='google_login'),
]
