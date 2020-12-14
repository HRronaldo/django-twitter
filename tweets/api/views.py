from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import (
    TweetSerializer,
    TweetCreateSerializer,
    TweetSerializerForDetail,
)
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params


class TweetViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        # <HOMEWORK> 通过某个 query 参数 with_comments 来决定是否需要带上 comments
        tweet = self.get_object()
        return Response(
            TweetSerializerForDetail(tweet).data,
            status=status.HTTP_200_OK,
        )

    @required_params(params=['user_id'])
    def list(self, request, *args, **kwargs):
        """
        这句查询会被翻译为
        select * from twitter_tweets
        where user_id = xxx
        order by created_at desc
        这句 SQL 查询会用到 user 和 created_at 的联合索引
        单纯的 user 索引是不够的
        """
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        # 一般来说 json 格式的 response 默认都要用 hash 的格式
        # 而不能用 list 的格式（约定俗成）
        return Response({'tweets': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(
            TweetSerializer(tweet).data,
            status=status.HTTP_201_CREATED,
        )

    # <HOMEWORK> 增加一个 like 的方法让用户可以通过 /api/tweets/<id>/like/ 点赞
    # <HOMEWORK> 增加一个 unlike 的方法让用户可以通过 /api/tweets/<id>/unlike/ 取消点赞
