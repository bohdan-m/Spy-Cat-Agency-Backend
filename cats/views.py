from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SpyCat
from .serializers import SpyCatSerializer, SpyCatUpdateSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SpyCatUpdateSerializer
        return SpyCatSerializer

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(
                {"detail": "Full updates not allowed. Use PATCH to update salary only."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)