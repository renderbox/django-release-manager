from django import template
from releasemanager.models import Release, Package
from django.utils import timezone

register = template.Library()


@register.inclusion_tag("releasemanager/release_template.html")
def release_packages(package_key, release_state=None, file_types=None):
    # Tag Inputs
    # - Package key
    # - Release State (optional) - Lock the rendering to only the release state specified (like '1' -> production),
    #   otherwise let the group settings decide
    # - Parts (optional) - Limit the rendering to only the parts specified (like 'css' and 'js')

    # Check to see if a user is in a group and if so get the latest release for that group

    # # If not in a group, get the latest published release for the package
    # # get the latest release based on the newest release marked as PRODUCTION
    # release = Release.objects.filter(state=Release.PRODUCTION).first()

    # [{file_type: "css", path:"/static/css/v0.1.0/main.css"}, {file_type:"js", path:"/static/js/v0.1.0/main.js"}]

    # # Process the 'files' field and return context to be used in the template
    # files = (
    #     release.files
    # )  # Assuming 'files' is a JSON field containing file information
    # return {"files": files}

    if file_types:
        file_types = file_types.split(",")
        # Convert the comma seperated string into a list

    try:
        package = Package.objects.get(package_key=package_key)

        # Get the current user's release group settings for the current site

        # If the user's group has a release newer than the current production release, use that release instead

        # DEFAULT: Retrieve the latest release for the specified package
        # current_date = timezone.now().date()
        # release = Release.objects.filter(
        #     package=package,
        #     release_date__lte=current_date,
        # )
        release = Release.objects.filter(
            package=package,
        )

        # Optionally filter by release state
        if release_state:
            # This needs to come from the model
            release = release.filter(state=int(release_state)).first()
        else:
            release = release.filter(state=1).first()
            # The assumption is that 1 is the production state, need to move this to the settings

        if not release:
            return {"files": []}

        # Optionally filter the release files by parts
        if file_types is not None:
            files = [f for f in release.files if f["file_type"] in file_types]
        else:
            files = release.files  # Use all files if 'parts' is not specified

        return {"files": files}
    except (Package.DoesNotExist, Release.DoesNotExist):
        return {"files": []}
