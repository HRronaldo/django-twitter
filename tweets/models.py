from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from likes.models import Like
from photos.models import Photo


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photos = models.ManyToManyField(Photo, blank=True)

    class Meta:
        index_together = (('user', 'created_at'),)

    def __str__(self):
        # 这里是你执行print(tweet instance) 的时候会显示的内容
        return '{} {}: {}'.format(self.created_at, self.user, self.content)

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id=self.id,
        ).order_by('-created_at')
