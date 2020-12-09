from accounts.api.serializers import UserSerializer, SignupSerializer, LoginSerializer
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.models import User
from rest_framework import permissions      
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited. 
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def get_serializer_class(self):
        if self.action == 'signup':
            return SignupSerializer
        return LoginSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            })
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({
            "success": True
        })
    
    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Plase check input",
                "errors": serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            "success": True
        })
