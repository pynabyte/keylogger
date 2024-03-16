from rest_framework import serializers
from user_management.models import User

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email',"password"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',"full_name","password"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password2")

        if password!=password2:
            raise serializers.ValidationError({"password":"Password and Confirm Password does not match"})
        return attrs
    
    def create(self,valid_data):
        return User.objects.create_user(**valid_data)