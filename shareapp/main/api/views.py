from django.http import HttpResponseRedirect, FileResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from shareapp.main.api.serializers import SharedItemSerializer, RetrievalSerializer
from shareapp.main.models import SharedItem, item_retrieved, Retrieval


class SharedItemViewSet(viewsets.ModelViewSet):
    serializer_class = SharedItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.request.user.shared_items.all().order_by("-created")


class SharedItemRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SharedItemSerializer
    permission_classes = [AllowAny]
    queryset = SharedItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return Response(status=HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["get"])
    def get(self, request, pk):
        item = SharedItem.objects.get(id=pk)
        password = request.headers.get("X-Password")
        if password != item.password:
            return Response(
                data={"details": _("Incorrect password or no password given.")},
                status=HTTP_403_FORBIDDEN,
            )
        elif item.is_expired:
            return Response(
                data={"details": _("This item has expired.")}, status=HTTP_403_FORBIDDEN
            )
        else:
            return self.handle_retrieval(item)

    def handle_retrieval(self, item: SharedItem):
        item_retrieved.send(sender=self.__class__, item_id=item.id)
        if item.url:
            return HttpResponseRedirect(item.url)
        else:
            return FileResponse(item.file, as_attachment=True)


class StatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RetrievalSerializer
    permission_classes = [IsAuthenticated]
    queryset = Retrieval.objects.all().order_by("created")

    def list(self, request, *args, **kwargs):
        data = {}
        for item in self.queryset.filter(user=self.request.user):
            data[item.created.strftime("%Y-%m-%d")] = {
                "files": item.files,
                "links": item.links,
            }
        return Response(data=data)
