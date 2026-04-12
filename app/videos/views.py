from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer

# Create your views here.


def ok(content=None):
    return Response(str(content) if content else "ok")


class VideosViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    @action(methods=["post", "delete"], detail=True)
    def likes(self, request, pk=None):
        return ok(pk)

    @action(methods=["get"], detail=False)
    def ids(self, request):
        return ok()

    @action(methods=["get"], detail=False, url_path="statistics-subquery")
    def statistics_subquery(self, request):
        return ok()

    @action(methods=["get"], detail=False, url_path="statistics-group-by")
    def statistics_group_by(self, request):
        return ok()
