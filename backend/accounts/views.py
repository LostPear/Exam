from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer,
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)
        return Response({'token': str(token), 'user': UserSerializer(user).data})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # For simplicity, stateless JWT logout (client discards token)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')
        if username:
            user.username = username
        if email is not None:
            user.email = email
        user.save()
        if phone is not None:
            profile = getattr(user, 'profile', None)
            if profile:
                profile.phone = phone
                profile.save()
        return Response({'message': '个人资料更新成功'})

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data['currentPassword']
        new_password = serializer.validated_data['newPassword']
        user: User = request.user
        if not user.check_password(current_password):
            return Response({'message': '当前密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.last_login = timezone.now()
        user.save()
        return Response({'message': '密码修改成功'})
