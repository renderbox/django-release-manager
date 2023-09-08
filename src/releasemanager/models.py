# import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# from django.utils.translation import gettext as _

from django.contrib.sites.models import Site


class ReleaseManager(models.Manager):
    def get_latest_release_for_package_and_user(self, package, user):
        """
        Get the latest release for a specified package within the user's release groups.
        """

        # if package is a string, get the package object
        if isinstance(package, str):
            package = Package.objects.get(package_key=package)

        current_datetime = timezone.now()

        default_id = getattr(settings, "RELEASE_MANAGER_DEFAULT_STATE", 1)

        current_site = Site.objects.get_current()

        latest_release = self.filter(
            Q(package=package),  # Filter the package
            (
                Q(release_groups__members=user)
                & Q(release_groups__sites=current_site)
                & Q(release_groups__active=True)
            )
            | (
                Q(release_date__lte=current_datetime) & Q(active=True)
            ),  # Get the latest published release, currently assumes default is ID 1 unless set in settings
        ).order_by("-release_date")

        return latest_release


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    package_key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def default_release_paths():
    return list([{"file_type": "css"}, {"file_type": "js"}])


class Release(models.Model):
    active = models.BooleanField(
        default=False, help_text="Is this release active for production?"
    )
    version = models.CharField(max_length=20)
    release_date = models.DateTimeField()
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="releases"
    )
    files = models.JSONField(
        blank=True,
        null=True,
        help_text="Nested type information for this release",
        default=default_release_paths,
    )

    objects = ReleaseManager()

    def __str__(self):
        return f"{self.package.name} - {self.version}"

    class Meta:
        ordering = ["-release_date"]
        unique_together = (("package", "version"),)
        # Makes sure there is only one entry of a given version per package


class ReleaseGroup(models.Model):
    """
    If a user is part of a Release Group, the newest release will be available for a given Package.

    If a user is not part of a group, they always get the latest release.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="release_groups", blank=True
    )
    active = models.BooleanField(default=False)
    sites = models.ManyToManyField(Site, related_name="releases", blank=True)
    releases = models.ManyToManyField(
        Release, related_name="release_groups", blank=True
    )

    def __str__(self):
        return self.name


"""
# Testing the release manager

from django import template
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from releasemanager.models import Release, Package

User = get_user_model()

package_key = "sample_app"
current_site = Site.objects.get_current()
user = User.objects.first()

Release.objects.get_latest_release_for_package_and_user(package_key, user)
"""
