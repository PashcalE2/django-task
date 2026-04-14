from logging import getLogger
from typing import Optional
from .exceptions import LikedAlreadyError, NoLikeError
from .models import Video, Like
from users.models import User
from django.db.models import Sum, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

logger = getLogger(__name__)


def _update_video_likes(video: Video, dif: int):
    video.total_likes += dif
    video.save(update_fields=["total_likes"])


def like_video(video: Video, user: User):
    logger.info(f"User ({user.pk}) likes Video ({video.id})")

    qs = Like.objects.get_queryset()
    like: Optional[Like] = qs.filter(video=video, user=user).first()
    if like is not None:
        raise LikedAlreadyError()
    qs.create(video=video, user=user)
    _update_video_likes(video, 1)


def unlike_video(video: Video, user: User):
    logger.info(f"User ({user.pk}) undoes like for Video ({video.id})")

    qs = Like.objects.get_queryset()
    like: Optional[Like] = qs.filter(video=video, user=user).first()
    if like is None:
        raise NoLikeError()
    qs.filter(video=video, user=user).delete()
    _update_video_likes(video, -1)
