from django.db.models import fields
from accounts.api.serializers import UserSerializer
from comments.api.serializers import CommentSerializer
from rest_framework import serializers
from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetSerializerWithComments(serializers.ModelSerializer):
    user = UserSerializer()
    # <HOMEWORK> 使用serializers.SerializerMethodField 的方式实现comments
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'comments', 'created_at', 'content')

    
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
