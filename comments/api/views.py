from comments.models import Comment
from comments.api.permissions import IsObjectOwner
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate
)
from django_filters.rest_framework import DjangoFilterBackend, filterset
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现list, create, update, destroy 的方法
    不实现retrieve（查询单个comment）的方法，因为没这个需求
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tweet_id']

    def get_permissions(self):
        # 注意要加用AllowAny() / IsAuthenticated() 实例化出对象
        # 而不是AllowAny / IsAuthenticated 这样只是一个类名
        if self.action == 'lsit':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['destroy', 'update']:
            return [IsAuthenticated(), IsObjectOwner()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        if 'tweet_id' not in request.query_params:
            return Response({
                'message': 'missing tweet_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(
            self.get_queryset()
        ).order_by('created_at')
        serializer = CommentSerializer(queryset, many=True)
        return Response({
            'comments': serializer.data,
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # 注意：这里必须要加'data=' 来指定参数是传给data 的
        # 因为默认的第一个参数是instance
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # save 方法会触发serializer 里的create 方法，点进save 的具体实现里面可以看到
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # get_object 是DRF 包装的一个函数，会在找不到的时候raise 404 error
        # 所以这里不需要再做额外的判断
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            raise Response({
            'message': 'Please check input'
        }, status=status.HTTP_400_BAD_REQUEST)
        # save 方法会触发serializer 里的update 方法，点进save 的具体实现你们可以看到
        # save 是根据instance 参数有没有传来决定是触发create 还是update
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        # DRF 里默认destroy 返回的是status code = 204 no content
        # 这里return 了success = True 更直观的让前端去做判断，所以return 200更合适
        return Response({'success': True}, status=status.HTTP_200_OK)
