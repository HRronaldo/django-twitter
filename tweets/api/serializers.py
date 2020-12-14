from accounts.api.serializers import UserSerializer
from comments.api.serializers import CommentSerializer
from django.contrib.contenttypes.models import ContentType
from likes.api.serializers import LikeSerializer
from likes.models import Like
from rest_framework import serializers
from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'user',
            'created_at',
            'content',
            'comments_count',
            'likes_count',
        )

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()


class TweetSerializerForDetail(TweetSerializer):
    # <HOMEWORK> 使用 serializers.SerializerMethodField 的方式实现 comments
    comments = CommentSerializer(source='comment_set', many=True)
    likes = LikeSerializer(source='like_set', many=True)

    class Meta:
        model = Tweet
        fields = (
            'id',
            'user',
            'comments',
            'created_at',
            'content',
            'likes',
            'comments',
            'likes_count',
            'comments_count',
        )


class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
