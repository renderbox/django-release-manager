from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .models import Package, ReleaseGroup, Release
from datetime import datetime, timedelta

"""
# Data Dump
./manage.py dumpdata --indent=4 -e contenttypes.contenttype -e admin -e sessions -e auth.permission -e core.releasemanageruser > ../src/releasemanager/fixtures/release_data.json
"""


class ReleaseGroupTestCase(TestCase):
    fixtures = ["sample_user.json", "release_data.json"]

    # def test_latest_release_in_release_group(self):
    #     # Get the latest release for the package in the user's release group
    #     latest_release = Release.objects.get_latest_release_for_package_and_user(
    #         self.package, self.user
    #     )

    #     # Ensure that the latest release is the future release
    #     self.assertEqual(latest_release, self.future_release)
