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

        # package = Package.objects.get(package_key=package_key)
        current_site = Site.objects.get_current()
        # current_datetime = timezone.now()

        # # active_release_groups = user.release_groups.filter(
        # #     sites=current_site, active=True
        # # )

        # # Get the latest available releasese in the active release groups

        # # 1) Get the current user's active release groups for the current site

        # # based on the provided package, get the latest release for the package that is in the user's release groups, including future release dates

        # release = (
        #     Release.objects.filter(
        #         package__release_groups__members=user,  # the release is in the user's release groups
        #         package__release_groups__sites=current_site,
        #         package__release_groups__active=True,  # Active release group
        #         # release_date__lte=current_datetime,  # Release date is in the past or now
        #     )
        #     .order_by("-release_date")
        #     .first()
        # )

        # # 2) If the user has a release group, get the latest release for the package that is in the user's release groups, including future release dates

        # if not release:
        #     # 3) If the user is not in a release group, get the latest release for the package (DEFAULT)
        #     # DEFAULT: Retrieve the latest default release for the specified package and ignore future release dates
        #     release = (
        #         Release.objects.filter(
        #             package=package,
        #             release_date__lte=current_datetime,
        #             state=1,
        #         )
        #         .order_by("-release_date")
        #         .first()
        #     )

        # Search for the package releases
        # check that the package is in the user's release groups
        #

        # filters = (Q(package=package), (Q(package__release_groups__members=user)))  # Filter the package

        # Q(package__release_groups__members=user)
        # | (Q(release_date__lte=current_datetime) & Q(state__release_state_id=1)),
        #     | Q(release_date__gt=current_datetime)
        # )

        # TODO: Query for results based on the user's release groups

        # DEFAULT: Retrieve the latest default ("production") release for the specified package and ignore future release dates
        latest_release = self.filter(
            Q(package=package),  # Filter the package
            Q(release_date__lte=current_datetime),
            Q(state__id=1),  # Assumes default is ID 1
        ).order_by("-release_date")

        # If there is no release, return the default release

        return latest_release


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    package_key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ReleaseState(models.Model):
    name = models.CharField(max_length=100)
    release_state_key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


def default_release_paths():
    return list([{"file_type": "css"}, {"file_type": "js"}])


class Release(models.Model):
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
    state = models.ForeignKey(ReleaseState, on_delete=models.CASCADE)

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
    release_state = models.ForeignKey(ReleaseState, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site, related_name="releases", blank=True)
    packages = models.ManyToManyField(Package, related_name="release_groups")
    # If no sites are specified, the group is applicable on all sites

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
