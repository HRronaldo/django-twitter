from accounts.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited. 
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
