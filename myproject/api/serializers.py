from rest_framework import serializers
from myapp.models import User,History
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirmpassword=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["email","name","password","confirmpassword"]
    
    def validate(self,data):
        password=data["password"]
        confirmpassword=data["confirmpassword"]
        if password!=confirmpassword:
            raise serializers.ValidationError("Passwords do not match")
        return data
    def create(self,validated_data):
        user=User.objects.create_user(email=validated_data["email"],name=validated_data["name"],password=validated_data["password"])
        return user
    
    
class ForgotPasswordRequest(serializers.Serializer):
    email=serializers.EmailField()

    def validate(self, data):
        email=data["email"]
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with the given mail do not exist")
        return data
    
class ForgotPasswordSuccess(serializers.Serializer):
    uidb64=serializers.CharField()
    token=serializers.CharField()
    password=serializers.CharField(write_only=True)
    confirmpassword=serializers.CharField(write_only=True)
    def validate(self,data):
        password=data["password"]
        confirmpassword=data["confirmpassword"]
        uid = force_str(urlsafe_base64_decode(data['uidb64']))
        user = User.objects.get(id=uid)
        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")
        if password!=confirmpassword:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(data['password'])
        user.save()
        return data
    


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        try:
            # Validate token
            RefreshToken(self.token)
        except TokenError:
            raise ValidationError("Invalid or expired refresh token")

        return attrs

    def save(self):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise ValidationError("Token already blacklisted or invalid")
        

class HistorySerializer(serializers.ModelSerializer):
    datetime=serializers.DateTimeField(read_only=True)
    class Meta:
        model=History
        fields=["id","job","exp","response","datetime"]