from django.test import TestCase

# from django.urls import reverse
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

# from django.conf import settings

from django.contrib.sites.models import Site

from .models import Release, Status

# from django.utils import timezone

# from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()

"""
# Data Dump
./manage.py dumpdata --indent=4 -e contenttypes.contenttype -e admin -e sessions -e auth.permission -e core.releasemanageruser > ../src/releasemanager/fixtures/release_data.json # noqa
"""


class ReleaseGroupTestCase(TestCase):
    fixtures = ["sample_user.json", "release_data.json"]

    def setUp(self):  # Set up data for the whole TestCase
        self.package_key = "basic"  # the name of the test package
        self.site = Site.objects.get_current()

        # an average user for testing permissions
        self.sampleuser = User.objects.get(username="sampleuser")

        # a developer user for testing permissions
        self.devuser = User.objects.get(username="devuser")

        # a release user for testing API permissions
        self.releaseuser = User.objects.get(username="releaseuser")

        # add the devuser to the test_group
        self.test_group = Group.objects.get(name="test_group")
        self.test_group.user_set.add(self.devuser)

    # What is the most current release the user can see
    def test_get_default_global_release(self):
        """Test that a user without special access gets the latest released globally."""

        site = Site.objects.get(pk=1)
        release = Release.objects.get(pk=3)  # v0.1.1

        accessible_release = (
            Release.objects.get_latest_release_for_package_site_and_user(
                self.sampleuser, site, self.package_key
            )
        )
        self.assertEqual(accessible_release, release)

    def test_get_default_site_release(self):
        """Test that a user without special access gets the latest released on the site."""
        site = Site.objects.get(pk=2)
        release = Release.objects.get(pk=5)  # v0.1.2

        accessible_release = (
            Release.objects.get_latest_release_for_package_site_and_user(
                self.sampleuser, site, self.package_key
            )
        )
        self.assertEqual(accessible_release, release)

    def test_get_dev_global_release(self):
        """Test that a user with special access gets the latest development release that is only available on the site."""
        site = Site.objects.get(pk=1)
        release = Release.objects.get(pk=2)  # v3.0.0

        accessible_release = (
            Release.objects.get_latest_release_for_package_site_and_user(
                self.devuser, site, self.package_key
            )
        )
        self.assertEqual(accessible_release, release)

    def test_get_dev_site_release(self):
        """Test that a user with special access gets the latest development release that is available globally."""

        site = Site.objects.get(pk=2)
        release = Release.objects.get(pk=4)  # v2.0.0

        accessible_release = (
            Release.objects.get_latest_release_for_package_site_and_user(
                self.devuser, site, self.package_key
            )
        )
        self.assertEqual(accessible_release, release)


class ReleaseAPITests(APITestCase):
    fixtures = ["sample_user.json", "release_data.json"]

    def setUp(self):  # Set up data for the whole TestCase
        self.package_key = "basic"  # the name of the test package
        self.site = Site.objects.get_current()

        # an average user for testing permissions
        self.sampleuser = User.objects.get(username="sampleuser")

        # a developer user for testing permissions
        self.devuser = User.objects.get(username="devuser")

        # a release user for testing API permissions
        self.releaseuser = User.objects.get(username="releaseuser")

        # On site ID 1, the current release is v0.1.1
        self.current_release = Release.objects.get(pk=3)

        # On site ID 1, the most current test release is v3.0.0
        self.beta_release = Release.objects.get(pk=2)

        # add the devuser to the test_group
        self.test_group = Group.objects.get(name="test_group")
        self.test_group.user_set.add(self.devuser)

        self.create_release_url = "/api/v1/releases/create/"

    # def test_releaseuser_can_not_delete_release(self):

    def test_releaseuser_create_release(self):
        """
        Ensure we can create a new release object.
        """
        # TODO: Should fail if the package key is not in the list of defined packages (aka, not a valid choice)
        data = {
            "package": "test_package",
            "version": "v1.1",
            "release_date": "2024-05-22T12:00:00Z",
            "status": Status.DEVELOPMENT,
            "release_notes": "Added new features.",
            "files": {"css": ["css/styles.css"]},
            "signature": "signature123",
        }
        # Set the user to the release user
        self.client.force_authenticate(user=self.releaseuser)
        response = self.client.post(self.create_release_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Release.objects.count(), 6)
        self.assertEqual(
            Release.objects.get(version="v1.1").release_notes, "Added new features."
        )

    def test_sampleuser_can_not_create_release(self):
        """
        Ensure a user without permission can not create a new release object.
        """

        data = {
            "package": "test_package",
            "version": "v1.1",
            "release_date": "2024-05-22T12:00:00Z",
            "status": Status.DEVELOPMENT,
            "release_notes": "Added new features.",
            "files": {"css": ["css/styles.css"]},
            "signature": "signature123",
        }
        # Set the user to the sample user
        self.client.force_authenticate(user=self.sampleuser)
        response = self.client.post(self.create_release_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#     def test_releaseuser_update_release(self):
#         """
#         Ensure we can add files to the 'files' field of a release.
#         """
#         data = {"files": {"js": ["js/bob.js"]}}
#         response = self.client.patch(
#             self.update_files_url(self.release.pk), data, format="json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_release = Release.objects.get(pk=self.release.pk)
#         self.assertIn("js/bob.js", updated_release.files["js"])
