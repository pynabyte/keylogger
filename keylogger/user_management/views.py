from rest_framework.views import APIView
from rest_framework.response import Response as R
from rest_framework import status as s
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.serializers import LoginSerializer, RegisterSerializer,ProfileSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from urllib.parse import urlencode
from rest_framework import serializers
from django.conf import settings
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import User

# Create tokens manually for users
# From the original documentation from simple JWT


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['full_name'] = user.full_name
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return R({"token": token, "message": "Login Successful."}, s.HTTP_200_OK)

            # If login failed , return error message
            return R({"error": "Invalid Credentials"}, s.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return R({"token": token, "message": "Registration Succesful"}, s.HTTP_201_CREATED)
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileSerializer
    def get(self,request,format=None):
        user = request.user
        serializer = self.serializer_class(user,many=False,context={"request":request})
        return R(serializer.data,s.HTTP_200_OK)
    
    def patch(self,request,format=None):
        user = request.user
        serializer = self.serializer_class(user,data=request.data,partial=True,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return R(serializer.data,s.HTTP_200_OK)
        return R({"error":serializer.errors},s.HTTP_400_BAD_REQUEST)
    
def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token

class GoogleLogin(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data

        email = data.get("email")
        id = data.get("id")
        full_name = data.get("full_name")

        if not email or not id or not full_name:
            return R({"error":"Email or ID missing"},status=s.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=id) if User.objects.filter(email=email).exists() else User.objects.create_user(email=email,full_name=full_name,password=id)
        if user is not None:
            token = get_tokens_for_user(user)
            return R({"token": token, "message": "Login Successful."}, s.HTTP_200_OK)
        else:
            return R({"error":"Invalid Credentials"},status=s.HTTP_400_BAD_REQUEST)
