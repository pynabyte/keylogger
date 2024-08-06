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
from user_management.mixins import PublicApiMixin, ApiErrorsMixin
from user_management.utils import google_get_access_token, google_get_user_info
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


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'
    
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google/'
        access_token = google_get_access_token(code=code, 
                                               redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return R(response_data)
        except User.DoesNotExist:
            full_name = user_data.get('full_name', '')

            user = User.objects.create(
                email=user_data['email'],
                full_name=full_name,
                registration_method='google',
            )
         
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return R(response_data)


