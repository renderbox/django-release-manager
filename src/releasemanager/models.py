from django.conf import settings
from django.db import models
from django.db.models import Q

# get User from the custom user model
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()


class Status(models.IntegerChoices):
    DEVELOPMENT = 1, "Development"
    TESTING = 10, "Testing"
    HOLD = 20, "Hold"
    RELEASED = 30, "Production"
    DEPRECATED = 40, "Deprecated"


class ReleaseManager(models.Manager):
    def get_accessible_releases(self, user, site, package):
        """Given a user, site & package key, return a queryset of releases that the user has access to."""

        # Only get the ueer's groups that have the special permissions
        user_groups = user.groups.filter(
            permissions__codename__in=[
                "can_access_test_release",
            ]
        ).distinct()

        # Get all releases for the package available to a site
        # This will pickup global releases and site-specific releases
        # If the release is group-specific, it will only be available to those groups
        releases = (
            self.get_queryset()
            .filter(
                (Q(sites=site) | Q(sites__isnull=True))
                & (Q(groups__in=user_groups) | Q(groups__isnull=True)),
                package=package,
                active=True,
            )
            .distinct()
        )

        # # Otherwise, filter the releases to those where the user's groups match
        # group_ids = user.groups.values_list("id", flat=True)
        # releases = queryset.filter(groups__id__in=group_ids).distinct()

        # if releases.exists():
        #     return releases.order_by("-release_date")

        # # If no group-specific or special permission releases are found, return the latest general release
        # return queryset.filter(status=Status.RELEASED).order_by("-release_date")

        return releases

    def get_latest_release_for_package_site_and_user(self, user, site, package):
        """Given a user, site & package key, return the most current release the user has access to."""
        return self.get_accessible_releases(user, site, package).first()
        # need to ingore any releases past the deprecation date


def default_release_paths():
    return list([{"file_type": "css"}, {"file_type": "js"}])


class Release(models.Model):
    active = models.BooleanField(
        default=False, help_text="Is this release active for production?"
    )
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.DEVELOPMENT,
        help_text="Current status of the release",
    )
    version = models.CharField(max_length=20)
    release_date = models.DateTimeField()
    deprecation_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the release is scheduled to be deprecated",
    )
    released_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who released the version",
    )
    release_notes = models.TextField(
        blank=True, help_text="Detailed notes about what is new, changed, or fixed"
    )
    package = models.CharField(  # defined in the settings so that it can be changed without changing the application
        # and be immutable at runtime
        max_length=100,
        choices=[(key, pkg["name"]) for key, pkg in settings.RM_PACKAGES.items()],
    )
    groups = models.ManyToManyField(
        Group, blank=True, help_text="User groups that can access this release"
    )
    sites = models.ManyToManyField(
        Site,
        blank=True,
        help_text="Sites where this release is isolated to.  If empty, it is available globally.",
    )
    files = models.JSONField(
        blank=True,
        null=True,
        help_text="Nested type information for this release",
        default=default_release_paths,  # Assuming a callable that returns a default dictionary to use
    )
    signature = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text="Digital signature for release integrity",
    )

    objects = ReleaseManager()

    def get_package_details(self):
        """Retrieve the package details from settings based on the package identifier."""
        return settings.RM_PACKAGES.get(self.package)

    class Meta:
        ordering = ["-version"]
        unique_together = (("package", "version"),)
        permissions = [
            ("can_test_releases", "Can access testing releases"),
        ]

    def __str__(self):
        package_details = self.get_package_details()
        return f"{package_details['name']} - {self.version}"


"""
# Testing the release manager

from django import template
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from releasemanager.models import Release, Package

User = get_user_model()

package = "sample_app"
current_site = Site.objects.get_current()
user = User.objects.first()

Release.objects.get_latest_release_for_package_and_user(package, user)
"""


"""
from releasemanager.models import Release
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
Release.objects.get_accessible_releases( user,1,"basic")
"""
