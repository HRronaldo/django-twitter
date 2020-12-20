from accounts.api.serializers import UserSerializerForComment
from comments.models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.models import Tweet


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForComment()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.like_set.count()

    class Meta:
        model = Comment
        fields = (
            'id', 
            'tweet_id', 
            'user', 
            'content', 
            'created_at',
            'likes_count',
        )


class CommentSerializerForCreate(serializers.ModelSerializer):
    # 这两项必须手动添加
    # 因为默认ModelSerializer 里只会自动包含user 和tweet 而不是user_id 和tweet_id
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')
    
    def validate(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({'message': 'tweet does not exist.'})
        # 必须return validated data
        # 也就是验证过之后，进行处理的（当然也可以不做处理）输入数据
        return data
    
    def create(self, validated_data):
        return Comment.objects.create(
            user_id = validated_data['user_id'],
            tweet_id = validated_data['tweet_id'],
            content = validated_data['content'],
        )


class CommentSerializerForUpdate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)
    
    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        # update 方法要求return 修改后的instance 作为返回值
        return instance
