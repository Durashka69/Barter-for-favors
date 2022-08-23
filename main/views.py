from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from main.models import (
    Category, Favor, User,
    Raiting, Request_Favor,
    Subcategory
)

from main.serializers import (
    FavorSerializer, UserSerializer,
    RaitingSerializer, CategorySerializer,
    Request_FavorSerializer, SubcategorySerializer,
)

from main.permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly
from main.filters import FavorFilter, SubcategoryFilter

from django_filters.rest_framework import DjangoFilterBackend


class FavorViewSet(viewsets.ModelViewSet):
    queryset = Favor.objects.all()
    serializer_class = FavorSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavorFilter

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class RaitingViewSet(viewsets.ModelViewSet):
    queryset = Raiting.objects.all()
    serializer_class = RaitingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class Request_FavorViewSet(CreateAPIView):
    queryset = Request_Favor.objects.all()
    serializer_class = Request_FavorSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class SubcategotyViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubcategoryFilter
