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
    like: Optional[Like] = Like.objects.filter(video=video, user=user).first()
    if like is not None:
        raise LikedAlreadyError()
    Like.objects.create(video=video, user=user)
    _update_video_likes(video, 1)


def unlike_video(video: Video, user: User):
    logger.info(f"User ({user.pk}) undoes like for Video ({video.id})")
    like: Optional[Like] = Like.objects.filter(video=video, user=user).first()
    if like is None:
        raise NoLikeError()
    Like.objects.filter(video=video, user=user).delete()
    _update_video_likes(video, -1)


def get_ids(video_qs):
    return video_qs.values_list("id", flat=True)


def statistics_subquery():
    data = (
        User.objects.annotate(
            likes=Coalesce(
                Subquery(
                    Video.objects.filter(owner_id=OuterRef("id"))
                    .values("owner_id")
                    .annotate(sum_likes=Sum("total_likes"))
                    .values("sum_likes")
                ),
                Value(0),
            )
        )
        .values("id", "likes")
        .order_by("id")
    )
    return data


def statistics_group_by():
    """
    data = (
        User.objects.annotate(likes=Sum("video__total_likes"))
        .values("id", "likes")
        .order_by("id")
    )
    """
    data = (
        User.objects.select_related()
        .annotate(likes=Sum("video__total_likes"))
        .values("id", "likes")
        .order_by("id")
    )

    return data
