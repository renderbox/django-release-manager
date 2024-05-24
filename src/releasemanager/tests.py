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

    def setUp(self):  # Set up data for the whole TestCase
        self.package_key = "basic"  # the name of the test package
        self.site = Site.objects.get_current()

        # an average user for testing permissions
        self.sampleuser = User.objects.get(username="sampleuser")

        # a developer user for testing permissions
        self.devuser = User.objects.get(username="devuser")

        # a release user for testing API permissions
        self.releaseuser = User.objects.get(username="releaseuser")

        # On site ID 1, the current release is 1.0
        self.current_release = Release.objects.get(pk=1)
        self.beta_release = Release.objects.get(pk=3)

    # What is the most current release the user can see
    def test_get_accessible_release_without_permission(self):
        # User without special access gets the latest released version
        accessible_release = Release.objects.get_accessible_release(
            self.sampleuser, self.site, self.package_key
        )
        self.assertEqual(accessible_release, self.current_release)

    def test_get_accessible_release_with_permission(self):
        # User with special access permission should get the latest release
        accessible_release = Release.objects.get_accessible_release(
            self.devuser, self.site, self.package_key
        )
        self.assertEqual(accessible_release, self.beta_release)

    # def test_devuser_has_permission_for_specific_package_version(self):

    # def test_sampleuser_fallback_to_general_release(self):

    # def test_newest_production_is_always_latest(self):


# class ReleaseAPITests(APITestCase):
#     fixtures = ["sample_user.json", "release_data.json"]

#     def setUp(self):  # Set up data for the whole TestCase
#         self.package_key = "basic"  # the name of the test package
#         self.site = Site.objects.get_current()

#         # an average user for testing permissions
#         self.sampleuser = User.objects.get(username="sampleuser")

#         # a developer user for testing permissions
#         self.devuser = User.objects.get(username="devuser")

#         # a release user for testing API permissions
#         self.releaseuser = User.objects.get(username="releaseuser")

#         # On site ID 1, the current release is 1.0
#         self.current_release = Release.objects.get(pk=1)
#         self.beta_release = Release.objects.get(pk=3)

# def test_releaseuser_can_not_delete_release(self):

#     def test_releaseuser_create_release(self):
#         """
#         Ensure we can create a new release object.
#         """
#         data = {
#             "package": "test_package",
#             "version": "1.1",
#             "release_date": "2024-05-22T12:00:00Z",
#             "status": Status.RELEASED,
#             "release_notes": "Added new features.",
#             "files": {"css": ["css/styles.css"]},
#             "signature": "signature123",
#         }
#         response = self.client.post(self.create_release_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Release.objects.count(), 2)
#         self.assertEqual(
#             Release.objects.get(version="1.1").release_notes, "Added new features."
#         )

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
