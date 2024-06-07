from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Release
from django.contrib.sites.models import Site


class ReleaseManagerMixin:
    """A mixin to provide the latest release for each package in the packages list to the context of a view."""

    packages = ["basic", "advanced", "enterprise"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        site = Site.objects.get_current()

        for item in self.packages:
            context["package_" + item] = (
                Release.objects.get_latest_release_for_package_site_and_user(
                    user, site, item
                )
            )

        return context


class ReleaseManagerIndexView(TemplateView):
    template_name = "releasemanager/index.html"


class ReleaseListView(LoginRequiredMixin, TemplateView):
    template_name = "releasemanager/list_releases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # site = self.request.get_current_site()
        site = Site.objects.get_current()

        # Fetch all accessible releases for the current user
        releases = Release.objects.get_accessible_releases(
            user, site, "basic"
        )
        context["releases"] = releases
        return context
