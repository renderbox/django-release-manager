from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from releasemanager.models import Release
from .serializers import ReleaseSerializer, ReleaseFileSerializer


class ReleaseListView(ListAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    permission_classes = [
        IsAuthenticated  # Only authenticated users can access this endpoint
    ]


class ReleaseCreateView(CreateAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    permission_classes = [
        DjangoModelPermissions,  # Ensure only users with the correct permissions can create a release
    ]

    def perform_create(self, serializer):
        # Additional logic before saving, if necessary
        serializer.save(released_by=self.request.user)


class ReleaseFileUpdateView(UpdateAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseFileSerializer
    permission_classes = [IsAuthenticated]  # Optionally, add more specific permissions
    lookup_field = "pk"  # Use the primary key to identify the release to update

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
