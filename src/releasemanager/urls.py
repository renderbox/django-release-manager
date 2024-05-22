from django.urls import path

from releasemanager import views

urlpatterns = [
    path("", views.ReleaseManagerIndexView.as_view(), name="releasemanager_index"),
    path(
        "packages/<str:package_key>/",
        views.PackageReleasesView.as_view(),
        name="package_releases",
    ),
]
