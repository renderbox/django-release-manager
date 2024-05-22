from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings

from django.contrib.sites.models import Site
from .models import Release, Status
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()

"""
# Data Dump
./manage.py dumpdata --indent=4 -e contenttypes.contenttype -e admin -e sessions -e auth.permission -e core.releasemanageruser > ../src/releasemanager/fixtures/release_data.json # noqa
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


class ReleaseAPITests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Set up package data in settings
        settings.RM_PACKAGES = {"test_package": {"name": "Test Package"}}

        # URL for creating releases
        self.create_release_url = reverse("api_create_release")

        # URL for updating files in a release
        self.update_files_url = lambda pk: reverse(
            "api_update_files", kwargs={"pk": pk}
        )

        # Create a release to be updated
        self.release = Release.objects.create(
            package="test_package",
            version="1.0",
            release_date="2024-05-21T12:00:00Z",
            status=Status.RELEASED,
            release_notes="Initial release.",
            files={},
        )

    def test_create_release(self):
        """
        Ensure we can create a new release object.
        """
        data = {
            "package": "test_package",
            "version": "1.1",
            "release_date": "2024-05-22T12:00:00Z",
            "status": Status.RELEASED,
            "release_notes": "Added new features.",
            "files": {"css": ["css/styles.css"]},
            "signature": "signature123",
        }
        response = self.client.post(self.create_release_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Release.objects.count(), 2)
        self.assertEqual(
            Release.objects.get(version="1.1").release_notes, "Added new features."
        )

    def test_update_release_files(self):
        """
        Ensure we can add files to the 'files' field of a release.
        """
        data = {"files": {"js": ["js/bob.js"]}}
        response = self.client.patch(
            self.update_files_url(self.release.pk), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_release = Release.objects.get(pk=self.release.pk)
        self.assertIn("js/bob.js", updated_release.files["js"])
