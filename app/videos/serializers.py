from rest_framework import serializers
from .models import Video, VideoFile
from users.serializers import UserSerializer


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = (
            "file",
            "quality",
        )


class VideoSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    files = VideoFileSerializer(many=True, allow_null=True)

    class Meta:
        model = Video
        fields = (
            "owner",
            "name",
            "total_likes",
            "created_at",
            "files",
            "is_published",
        )
