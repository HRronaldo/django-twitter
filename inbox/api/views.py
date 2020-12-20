from django.db.models.aggregates import Count
from inbox.api.serializers import (
    NotificationSerializer,
    NotificationSerializerForUpdate,
)
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.decorators import required_params


class NotificationViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()

    @action(methods=['GET'], detail=False)
    def unread_count(self, request, *args, **kwargs):
        count = self.get_queryset().count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)

    @required_params(method='POST', params=['unread'])
    def update(self, request, *args, **kwargs):
        """
        用户可以标记一个notification 为已读或者未读。标记已读和未读都是对notification
        的一次更新操作，所以直接重载update 的方法来实现。另外一种实现方法是用一个专属的action：
            @action(methods=['POST'], detail=True, url_path='mark-as-read')
            def mark_as_read(self, request, *args, **kwargs):
                ...
            @action(methods=['POST'], detail=True, url_path='mark-as-unread')
            def mark_as_unread(self, request, *args, **kwargs):
                ...
        两种方法都可以，我更偏好重载update，因为更通用更rest 一些, 而且mark as unread 和
        mark as read 可以公用一套逻辑。
        """
        serializer = NotificationSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        notification = serializer.save()
        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_200_OK,
        )