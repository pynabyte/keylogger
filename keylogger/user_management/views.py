from rest_framework.views import APIView
from rest_framework.response import Response as R
from rest_framework import status as s

class LoginView(APIView):
    def get(self,request):
        return R({"message":"Login Get Working"})