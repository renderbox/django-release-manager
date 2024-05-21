from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings

from django.contrib.sites.models import Site
from .models import Release, Status
from django.utils import timezone

User = get_user_model()

"""
# Data Dump
./manage.py dumpdata --indent=4 -e contenttypes.contenttype -e admin -e sessions -e auth.permission -e core.releasemanageruser > ../src/releasemanager/fixtures/release_data.json
"""


class ReleaseGroupTestCase(TestCase):
    fixtures = ["sample_user.json", "release_data.json"]

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.site = Site.objects.create(domain="example.com", name="Example")
        cls.group = Group.objects.create(name="Test Group")
        cls.user.groups.add(cls.group)
        cls.permission = Permission.objects.create(
            codename="special_access", name="Can View Special Releases"
        )
        cls.group.permissions.add(cls.permission)

        cls.package_key = "test_package"
        settings.RM_PACKAGES = {cls.package_key: {"name": "Test Package"}}

        cls.release1 = Release.objects.create(
            package=cls.package_key,
            status=Status.RELEASED,
            version="1.0",
            release_date=timezone.now() - timezone.timedelta(days=1),
            sites=[cls.site],
            groups=[cls.group],
        )
        cls.release2 = Release.objects.create(
            package=cls.package_key,
            status=Status.DEVELOPMENT,
            version="2.0",
            release_date=timezone.now(),
            sites=[cls.site],
        )

    def test_get_accessible_release_with_permission(self):
        # User with special access permission should get the latest release
        self.user.user_permissions.add(self.permission)
        accessible_release = Release.objects.get_accessible_release(
            self.user, self.package_key
        )
        self.assertEqual(accessible_release, self.release2)

    def test_get_accessible_release_without_permission(self):
        # User without special access gets the latest released version
        accessible_release = Release.objects.get_accessible_release(
            self.user, self.package_key
        )
        self.assertEqual(accessible_release, self.release1)

    def test_get_accessible_releases_no_group_match(self):
        # Create a release that does not match user's group
        Release.objects.create(
            package=self.package_key,
            status=Status.TESTING,
            version="3.0",
            release_date=timezone.now(),
            sites=[self.site],
        )
        # User should still fall back to the latest released version
        accessible_releases = Release.objects.get_accessible_releases(
            self.user, self.package_key
        )
        self.assertIn(self.release1, list(accessible_releases))
        self.assertNotIn(self.release2, list(accessible_releases))

    def test_fallback_to_general_release(self):
        # Test that it falls back to the latest general release
        new_user = User.objects.create_user(username="newuser", password="12345")
        accessible_release = Release.objects.get_accessible_release(
            new_user, self.package_key
        )
        self.assertEqual(accessible_release, self.release1)
