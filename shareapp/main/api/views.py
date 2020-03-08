from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from shareapp.main.api.serializers import SharedItemSerializer


class SharedItemViewSet(viewsets.ModelViewSet):
    serializer_class = SharedItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.request.user.shared_items.all().order_by("-created")
