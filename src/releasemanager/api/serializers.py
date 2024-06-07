# --------------------------------------------
# Copyright 2023, Grant Viklund
# @Author: Grant Viklund
# @Date:   2023-09-06 12:26:10
# --------------------------------------------

from rest_framework import serializers
from releasemanager.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = ["name", "release_notes", "release_date", "status"]


class ReleaseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = ["files"]

    def update(self, instance, validated_data):
        files_data = validated_data.get("files", {})

        # Assuming `files` is already a dict if it exists
        if instance.files:
            # Update existing dictionary with new paths
            for key, value in files_data.items():
                if key in instance.files:
                    instance.files[key].extend(
                        value if isinstance(value, list) else [value]
                    )
                else:
                    instance.files[key] = value if isinstance(value, list) else [value]
        else:
            # Set new dictionary if none exists
            instance.files = files_data

        instance.save()
        return instance
