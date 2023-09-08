from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .models import Package, ReleaseState, ReleaseGroup, Release
from datetime import datetime, timedelta


class ReleaseGroupTestCase(TestCase):
    fixtures = ["release_data.json"]

    def setUp(self):
        User = get_user_model()

        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a release state
        self.release_state = ReleaseState.objects.create(
            name="Test Release State", release_state_key="test_state"
        )

        # Create a site
        self.site = Site.objects.create(name="Test Site", domain="test.com")

        # Create a package
        self.package = Package.objects.create(
            name="Test Package", package_key="test_package"
        )

        # Create a release group
        self.release_group = ReleaseGroup.objects.create(
            name="Test Release Group",
            description="Test description",
            active=True,
            release_state=self.release_state,
        )
        self.release_group.members.add(self.user)
        self.release_group.sites.add(self.site)
        self.release_group.packages.add(self.package)

        # Create a past release for the package
        self.past_release = Release.objects.create(
            version="1.0",
            release_date=datetime.now() - timedelta(days=7),
            package=self.package,
            state=self.release_state,
        )

        # Create a future release for the package
        self.future_release = Release.objects.create(
            version="2.0",
            release_date=datetime.now() + timedelta(days=7),
            package=self.package,
            state=self.release_state,
        )

    def test_latest_release_in_release_group(self):
        # Get the latest release for the package in the user's release group
        latest_release = Release.objects.get_latest_release_for_package_and_user(
            self.package, self.user
        )

        # Ensure that the latest release is the future release
        self.assertEqual(latest_release, self.future_release)
