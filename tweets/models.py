from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 这里是你执行 print(tweet instance) 的时候会显示的内容
        return '{} {}: {}'.format(self.created_at, self.user, self.content)
