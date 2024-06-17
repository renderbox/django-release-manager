from django.core.management.base import BaseCommand, CommandError

from releasemanager.models import Release

# django settings
from django.conf import settings


class Command(BaseCommand):
    help = "Registers a new release for a package"

    def add_arguments(self, parser):
        parser.add_argument("package_name", type=str, help="Name of the package")
        parser.add_argument("release_name", type=str, help="Name of the release")

    def handle(self, *args, **options):
        package_name = options["package_name"]
        release_name = options["release_name"]

        try:
            package = settings.RM_PACKAGES[package_name]
            release, created = Release.objects.get_or_create(
                name=release_name, package=package_name
            )

            if created:
                release.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully registered release {release_name} for package {package_name}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Release {release_name} for package {package_name} already exists."
                    )
                )

        except KeyError:
            raise CommandError(
                f'Package "{package_name}" does not exist.'
            )  # Only dictionary query is checing on the package so this works
