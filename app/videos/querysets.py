from django.db import models
from django.db.models import Q, Sum, OuterRef, F

from users.models import User


class VideoQuerySet(models.QuerySet):
    def published(self, user: User = None):
        if user is not None and user.is_authenticated:
            return self.filter(Q(owner=user) | Q(is_published=True))
        return self.filter(is_published=True)

    def statistics_subquery(self):
        return (
            self.published()
            .annotate(username=F("owner__username"))
            .values("username")
            .annotate(
                likes=Sum(
                    self.published()
                    .filter(owner=OuterRef("owner"))
                    .values("owner")
                    .annotate(likes=Sum("total_likes"))
                    .values("likes")
                ),
            )
            .order_by("-likes")
        )

    def statistics_group_by(self):
        return (
            self.published()
            .values("owner__username")
            .annotate(username=F("owner__username"), likes=Sum("total_likes"))
            .values("username", "likes")
            .order_by("-likes")
        )
