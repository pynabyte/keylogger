from user_management.views import LoginView,RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("login",LoginView.as_view(),name="login"),
    path("register",RegisterView.as_view(),name="register"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
