from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def ok(content=None):
    return HttpResponse(str(content) if content else "ok")


def get_by_id(request, video_id: int):
    return ok(video_id)


def get_all(request):
    return ok()


def get_likes(request, video_id: int):
    return ok(video_id)


def get_ids(request):
    return ok()


def statistics_subquery(request):
    return ok()


def statistics_group_by(request):
    return ok()
