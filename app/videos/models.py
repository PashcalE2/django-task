from django.db import models
from django.utils import timezone
from .querysets import VideoQuerySet


class Video(models.Model):
    owner = models.ForeignKey(
        "users.User", models.CASCADE, verbose_name="Владелец", related_name="videos"
    )
    is_published = models.BooleanField("Опубликовано", default=False)
    name = models.CharField("Название", max_length=255)
    total_likes = models.PositiveBigIntegerField("Число лайков", default=0)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)

    objects = VideoQuerySet.as_manager()

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = "HD", "720p"
        FHD = "FHD", "1080p"
        UHD = "UHD", "4k"

    pk = models.CompositePrimaryKey("video", "quality")
    video = models.ForeignKey(
        Video, models.CASCADE, verbose_name="Видео", related_name="files"
    )
    quality = models.CharField("Качество", choices=Quality.choices, default=Quality.HD)
    file = models.FileField("Файл", blank=True, null=True)

    def __str__(self):
        return f"{self.video.name}: {self.quality}"


class Like(models.Model):
    pk = models.CompositePrimaryKey("video", "user")
    video = models.ForeignKey(
        Video, models.CASCADE, verbose_name="Видео", related_name="likes"
    )
    user = models.ForeignKey(
        "users.User", models.CASCADE, verbose_name="Пользователь", related_name="likes"
    )

    def __str__(self):
        return f"{self.video.name}: {self.user.first_name}"
