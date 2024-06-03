from django.urls import path

from .views import ReleaseListView, ReleaseCreateView, ReleaseFileUpdateView

urlpatterns = [
    path("releases/", ReleaseListView.as_view(), name="api_releases"),
    path("releases/create/", ReleaseCreateView.as_view(), name="api_create_release"),
    path(
        "releases/<int:pk>/update_files/",
        ReleaseFileUpdateView.as_view(),
        name="api_update_files",
    ),
]
