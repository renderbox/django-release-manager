from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Release


class ReleaseManagerIndexView(TemplateView):
    template_name = "releasemanager/index.html"


class PackageReleasesView(LoginRequiredMixin, TemplateView):
    template_name = "releases/package_releases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_key = self.kwargs["package_key"]

        # Get all accessible releases for this package and the current user
        releases = Release.objects.get_accessible_releases(
            self.request.user, package_key
        )

        context.update({"package_key": package_key, "releases": releases})
        return context
