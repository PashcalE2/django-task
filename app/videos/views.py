from rest_framework import viewsets, permissions, status
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Video
from .serializers import VideoSerializer
import videos.services as services

# Create your views here.


def ok(content=None):
    return Response(str(content) if content else "ok")


class VideosViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action in ("likes", "ids"):
            return qs.published()

        qs = qs.prefetch_related("files")

        if not self.request.user.is_staff:
            return qs.published(self.request.user)

        return qs

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def likes(self, request: Request, pk=None):
        video = self.get_queryset().filter(pk=pk).get()

        if request.method == "POST":
            services.like_video(video, self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            services.unlike_video(video, self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise NotImplementedError(request.method)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAdminUser],
    )
    def ids(self, request: Request):
        return Response(
            self.get_queryset().values_list("id", flat=True),
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["get"],
        detail=False,
        url_path="statistics-subquery",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_subquery(self, request: Request):
        data = self.get_queryset().statistics_subquery()
        return Response(data, status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        url_path="statistics-group-by",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_group_by(self, request: Request):
        data = self.get_queryset().statistics_group_by()
        return Response(data, status.HTTP_200_OK)
