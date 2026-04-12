from rest_framework import serializers
from .models import Video, VideoFile, Like


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("pk", "owner", "is_published", "name", "total_likes", "created_at")


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ("pk", "video", "quality")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("pk", "video", "user")
