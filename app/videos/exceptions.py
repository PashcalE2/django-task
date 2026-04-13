from app.exceptions import AppError
from rest_framework import status


class LikedAlreadyError(AppError):
    status = status.HTTP_409_CONFLICT
    message = "This user has already liked the video"


class NoLikeError(AppError):
    status = status.HTTP_409_CONFLICT
    message = "This user has not yet liked the video"
