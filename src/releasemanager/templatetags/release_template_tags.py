from django import template
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone

from releasemanager.models import Release

register = template.Library()


@register.inclusion_tag("releasemanager/release_template.html")
def release_package(package, file_group):
    """
    Given a package object, extract the various file types.
    """

    files = []

    for file in package.files:
        if file["file_group"] == file_group:
            files.append(file)

    for file in files:
        file["file_ext"] = file["file_name"].split(".")[-1]

    return {"files": files}
