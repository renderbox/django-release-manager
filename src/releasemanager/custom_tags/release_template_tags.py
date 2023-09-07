from django import template
from releasemanager.models import Release, Package
from django.utils import timezone

register = template.Library()


@register.inclusion_tag("release_template.html")
def render_release_template(package_key, release_state=None, parts=None):
    # Tag Inputs
    # - Package key
    # - Release State (optional) - Lock the rendering to only the release state specified (like '1' -> production),
    #   otherwise let the group settings decide
    # - Parts (optional) - Limit the rendering to only the parts specified (like 'css' and 'js')

    # Check to see if a user is in a group and if so get the latest release for that group

    # # If not in a group, get the latest published release for the package
    # # get the latest release based on the newest release marked as PRODUCTION
    # release = Release.objects.filter(state=Release.PRODUCTION).first()

    # # Process the 'files' field and return context to be used in the template
    # files = (
    #     release.files
    # )  # Assuming 'files' is a JSON field containing file information
    # return {"files": files}

    if parts:
        parts = parts.split(",")

    try:
        package = Package.objects.get(package_key=package_key)

        # Get the current user's release group settings for the current site

        # If the user's group has a release newer than the current production release, use that release instead

        # DEFAULT: Retrieve the latest release for the specified package
        current_date = timezone.now().date()
        release = Release.objects.filter(
            package=package,
            release_date__lte=current_date,
        )

        # Optionally filter by release state
        if release_state is not None:
            release = release.filter(
                state=int(release_state)
            )  # This needs to come from the model
        else:
            release = release.filter(state=Release.PRODUCTION)

        # Optionally filter the release files by parts
        if parts is not None:
            filtered_files = {}
            for part in parts:
                if part in release.files:
                    filtered_files[part] = release.files[part]
            files = filtered_files
        else:
            files = release.files  # Use all files if 'parts' is not specified

        return {"files": files}
    except Package.DoesNotExist:
        return {"files": {}}
