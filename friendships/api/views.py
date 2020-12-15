from django import contrib
from django.contrib.admin import decorators
from django.contrib.auth.models import User
from friendships.api.serializers import (
    FollowerSerializer,
    FollowingSerialzier,
    FriendshipSerializerForCreate,
)
from friendships.models import Friendship
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class FriendshipViewSet(viewsets.GenericViewSet):
    # 我们希望POST /api/friendship/1/follow 是去follow user_id=1 的用户
    # 因此这里queryset 需要是User.objects.all()
    # 如果是Friendship.objects.all 的话就会出现404 Not Found
    # 因为detail=True 的actions 会默认先去调用get_object() 也就是
    # queryset.filter(pk=1) 查询一下这个object 在不在
    queryset = User.objects.all()

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowerSerializer(friendships, many=True)
        return Response(
            {'followers': serializer.data},
            status = status.HTTP_200_OK,
        )
    
    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        serializer = FollowingSerialzier(friendships, many=True)
        return Response(
            {'followings': serializer.data},
            status = status.HTTP_200_OK,
        )
    
    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        # 特殊判断重复follow 的情况（比如前端猛点好多少次follow)
        # 静默处理，不报错，因为这类重复操作因为网络延迟的原因会比较多，没必要当做错误处理
        if Friendship.objects.filter(from_user=request.user, to_user=pk).exists():
            return Response({
                'success': True,
                'duplicate': True,
            }, status=status.HTTP_201_CREATED)
        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': pk,
        })
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        # 注意pk 的类型是str，所以要做类型转换
        if request.user.id == int(pk):
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself',
            }, status=status.HTTP_400_BAD_REQUEST)
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#delete
        # Queryset 的delete 操作返回两个值，一个是删了多少数据，一个是具体每种类型删了多少
        # 为什么会出现多种类型数据的删除？因为可能因为foreign key 设置了cascade 出现级联删除，
        # 也就是比如A model 的某个属性是B model 的foreign key，并且设置了on_delete=models.CASCADE, 
        # 那么当B 的某个数据被删除的时候，A 中的关联也会被删除。所以CASCADE 是很危险的，
        # 我们一般最好不要用，而是用on_delete=models.SET_NULL取而代之，
        # 这样至少可以避免误删除操作带来的多米诺效应。
        deleted, _ = Friendship.objects.filter(
            from_user=request.user,
            to_user=pk,
        ).delete()
        return Response({'success': True, 'deleted': deleted})
