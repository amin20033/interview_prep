from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer,ForgotPasswordRequest,ForgotPasswordSuccess,LogoutSerializer,HistorySerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from myapp.models import User,History
from myapp.views import ask_ai
# Create your views here.

class RegisterView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

class HistoryView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        job=request.data.get("job")
        exp=request.data.get("exp")
        model=request.data.get("model")
        if job is None or exp is None or model is None:
            return Response({"status":"error","message":"job or exp or model can't be empty"},status=400)
        response=ask_ai(job,exp,model)
        response = response.replace("**", "")
        data={
            "job":job,
            "exp":exp,
            "response":response
        }
        serializer=HistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status":"success","data":serializer.data},status=201)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        history=History.objects.filter(user=request.user)
        serializer=HistorySerializer(history,many=True)
        return Response(serializer.data,status=200)

class ForgotPasswordRequestView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=ForgotPasswordRequest(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"

            send_mail(
                "Password Reset",
                f"Reset your password: {reset_link}",
                "iamaminurrahman2003@gmail.com",
                [user.email],
            )
            return Response({"message": "Reset link sent"},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordSuccessView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,uidb64,token): 
        data={
           "password":request.data.get("password"),
           "confirmpassword":request.data.get("confirmpassword"),
           "uidb64":uidb64,
           "token":token
            }
        serializer=ForgotPasswordSuccess(data=data)
        if serializer.is_valid():
            return Response({"message":"Password Changed Successfully"},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )

class DetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        try:
            history=History.objects.get(id=id)
        except:
            return Response({"status":"error","message":"Wrong id"},status=404)
        if history.user!=request.user:
            return Response({"status":"error","message":"Wrong id"},status=404)
        serializer=HistorySerializer(history)
        return Response(serializer.data,status=200)

    
