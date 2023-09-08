# import uuid

from django.conf import settings
from django.db import models

# from django.utils.translation import gettext as _

from django.contrib.sites.models import Site


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

    def __str__(self):
        return f"{self.package.name} - {self.version}"

    class Meta:
        ordering = ["-release_date"]
        unique_together = (
            (
                "package",
                "version",
            ),
        )
        # Makes sure there is only one entry of a given version per package


class ReleaseGroup(models.Model):
    """
    If a user is part of a Release Group, the newest release will be available for a given Package.

    If a user is not part of a group, they always get the latest release.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="release_groups"
    )
    active = models.BooleanField(default=False)
    release_state = models.ForeignKey(ReleaseState, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site, related_name="releases")
    # If no sites are specified, the group is applicable on all sites

    def __str__(self):
        return self.name
