from django.core.management.base import BaseCommand, CommandError

from releasemanager.models import Release

# django settings
from django.conf import settings


class Command(BaseCommand):
    help = "Registers a file under a specific release and package with optional additional fields"

    def add_arguments(self, parser):
        parser.add_argument("package_name", type=str, help="Name of the package")
        parser.add_argument("release_name", type=str, help="Name of the release")
        parser.add_argument("path", type=str, help="Path of the file to register")
        parser.add_argument(
            "--file_group",
            type=str,
            default=None,
            help="Optional: file group for categorization and use with template tags",
        )
        parser.add_argument(
            "--option",
            action="append",
            type=str,
            help="Optional key=value pairs to add as extra data",
        )

    def handle(self, *args, **options):
        package_name = options["package_name"]
        release_name = options["release_name"]
        path = options["path"]
        file_group = options.get("file_group")

        if not file_group:
            file_extension = path.split(".")[-1]  # Simple extraction of file extension
            file_group = file_extension  # Use the file extension as the file group

        options_list = options.get("option", [])

        try:
            package = settings.RM_PACKAGES[package_name]
            release = Release.objects.get(name=release_name, package=package)

            if not release.files:  # make sure the object is created
                release.files = {}

            if file_group not in release.files:
                release.files[file_group] = []

            options = {}

            # TODO:  Check if the file is already added.  Just update options if it is.

            if options_list:
                for option in options_list:
                    try:
                        key, value = option.split("=")
                        options[key] = value
                    except ValueError:
                        raise CommandError("Options must be in the format key=value")

            release.files[file_group].append({"path": path, "options": options})

            release.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully registered file at {path} under {file_group} in release {release_name} of package {package_name}."
                )
            )

        except KeyError:
            raise CommandError(
                f'Package "{package_name}" does not exist.'
            )  # Only dictionary query is checing on the package so this works
        except Release.DoesNotExist:
            raise CommandError(
                f'Release "{release_name}" for package "{package_name}" does not exist.'
            )
        except Exception as e:
            raise CommandError(f"Error registering file: {e}")
