from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # Django 还有一个ImageField，但是尽量不要用，会有很多的其他问题，用FileField 可以起到
    # 同样的效果。因为最后我们都是以文件形式存储起来，使用的是文件的url 进行访问
    avatar = models.FileField(null=True)
    # 当一个user 被创建之后，会创建一个user profile 的object
    # 此时用户还来不及去设置nickname 等信息，因此设置null=True
    nickname = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)
    

# 定义一个profile 的property 方法，植入到User 这个model 里
# 这样当我们通过user 的一个实例化对象访问profile 的时候，即user_instance.profile
# 就会在UserProfile 中进行get_or_create 来获得对应的profile 的object
# 这种写法实际上是一个利用Python 的灵活性进行hack 的方法，这样会方便我们通过user 快速
# 访问到对应的profile 信息。
def get_profile(user):
    if hasattr(user, '_cached_user_profile'):
        return getattr(user, '_cached_user_profile')
    profile, _=UserProfile.objects.get_or_create(user=user)
    # 使用user 对象的属性进行缓存(cache)，避免多次调用同一个user 的profile 时
    # 重复的对数据库进行查询
    setattr(user, '_cached_user_profile', profile)
    return profile


User.profile = property(get_profile)
