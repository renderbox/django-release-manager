from django import template
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone

from releasemanager.models import Release, Package

register = template.Library()


@register.inclusion_tag("releasemanager/release_template.html")
def release_packages(package_key, user=None, release_state=None, file_types=None):
    """
    Get the latest release for a specified package within the user's release groups.
    """

    if file_types:
        file_types = file_types.split(",")
        # Convert the comma seperated string into a list

    try:
        release = Release.objects.get_latest_release_for_package_and_user(
            package_key, user
        )

        # If there is still not a release available, return an empty list
        if release.count() == 0:
            return {"files": []}

        # Optionally filter the release files by parts
        if file_types is not None:
            files = [f for f in release.first().files if f["file_type"] in file_types]
        else:
            files = release.first().files  # Use all files if 'parts' is not specified

        return {"files": files}
    except (Package.DoesNotExist, Release.DoesNotExist):
        return {"files": []}
