from django.urls import path

from .views import ReleaseListView, ReleaseCreateView, ReleaseFileUpdateView

urlpatterns = [
    path("api/releases/", ReleaseListView.as_view(), name="api_releases"),
    path("api/releases/new/", ReleaseCreateView.as_view(), name="api_create_release"),
    path(
        "api/releases/<int:pk>/update_files/",
        ReleaseFileUpdateView.as_view(),
        name="api_update_files",
    ),
]
