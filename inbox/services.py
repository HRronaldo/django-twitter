from notifications.signals import notify
from django.contrib.contenttypes.models import ContentType
from tweets.models import Tweet
from comments.models import Comment


class NotificationService(object):

    @classmethod
    def send_like_notification(cls, like):
        target = like.content_object
        if like.content_type == ContentType.objects.get_for_model(Tweet):
            notify.send(
                like.user,
                recipient=target.user,
                verb='liked your tweet',
                target=target,
            )
        if like.content_type == ContentType.objects.get_for_model(Comment):
            notify.send(
                like.user,
                recipient=target.user,
                verb='liked your comment',
                target=target,
            )

    @classmethod
    def send_comment_notification(cls, comment):
        notify.send(
            comment.user,
            recipient=comment.tweet.user,
            verb='liked your comment',
            target=comment.tweet,
        )
