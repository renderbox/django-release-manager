from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Release
from django.contrib.sites.models import Site


class ReleaseManagerIndexView(TemplateView):
    template_name = "releasemanager/index.html"


# class PackageReleasesView(LoginRequiredMixin, TemplateView):
#     template_name = "releasemanager/package_releases.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         package_key = self.kwargs["package_key"]

#         # Get all accessible releases for this package and the current user
#         releases = Release.objects.get_accessible_releases(
#             self.request.user, package_key
#         )

#         context.update({"package_key": package_key, "releases": releases})
#         return context


class ReleaseListView(LoginRequiredMixin, TemplateView):
    template_name = "releasemanager/list_releases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # site = self.request.get_current_site()
        site = Site.objects.get_current()

        # Fetch all accessible releases for the current user
        releases = Release.objects.get_accessible_releases(user, site, "basic")
        context["releases"] = releases
        return context
