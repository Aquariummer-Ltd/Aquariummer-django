from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Fish

from aquarium import serializers


class BaseAquariumAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Base viewset for user owned aquarium attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class FishViewSet(BaseAquariumAttrViewSet):
    """Manage fishes in the database"""
    queryset = Fish.objects.all()
    serializer_class = serializers.FishSerializer
