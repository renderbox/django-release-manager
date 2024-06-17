from django.core.management.base import BaseCommand

from releasemanager.models import Release, Status

# django settings
from django.conf import settings


class Command(BaseCommand):
    help = "Lists all packages defined in settings.RM_PACKAGES"

    def handle(self, *args, **options):
        packages = getattr(settings, "RM_PACKAGES", {})
        if packages:
            self.stdout.write(
                self.style.SUCCESS(
                    "Listing all configured packages and their active releases:"
                )
            )
            for key, details in packages.items():
                self.stdout.write(f'Package key: {key}, Name: {details.get("name")}')
                # Fetch active releases for this package key
                active_releases = Release.objects.filter(package=key, active=True)
                if active_releases.exists():
                    self.stdout.write("\tActive Releases:")
                    for release in active_releases:
                        if release.status == Status.RELEASED:
                            self.stdout.write(
                                self.style.SUCCESS(f"\t\tVersion: {release.name}*")
                            )
                        elif (
                            release.status == Status.TESTING
                            or release.status == Status.DEVELOPMENT
                        ):
                            self.stdout.write(
                                self.style.WARNING(f"\t\tVersion: {release.name}")
                            )
                        elif release.status == Status.DEPRECATED:
                            self.stdout.write(
                                self.style.ERROR(f"\t\tVersion: {release.name}~")
                            )
                        else:
                            self.stdout.write(f"\t\tVersion: {release.name}")
                else:
                    self.stdout.write("\tNo active releases")
        else:
            self.stdout.write(
                self.style.WARNING("No packages defined in settings.RM_PACKAGES.")
            )
