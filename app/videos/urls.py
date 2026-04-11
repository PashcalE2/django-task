from django.urls import path

from . import views

urlpatterns = [
    path("<int:video_id>/", views.get_by_id),
    path("", views.get_all),
    path("<int:video_id>/likes/", views.get_likes),
    path("ids/", views.get_ids),
    path("statistics-subquery/", views.statistics_subquery),
    path("statistics-group-by/", views.statistics_group_by),
]
