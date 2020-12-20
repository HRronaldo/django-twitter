from accounts.api.serializers import UserSerializer
from notifications.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()

    class Meta:
        model = Notification
        fields = (
            'id',
            'recipient',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'action_object_content_type',
            'action_object_object_id',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'unread',
        )


class NotificationSerializerForUpdate(serializers.ModelSerializer):
    # BooleanField 会自动兼容unread=true, false, "true", "false", "True", "1", "0"
    # 等情况，并都转换为python 的boolean 类型的True / False
    unread = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ('unread',)

    def update(self, instance, validated_data):
        instance.unread = validated_data['unread']
        instance.save()
        return instance
