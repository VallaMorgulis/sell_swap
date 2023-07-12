from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import serializers
from .models import Product, ProductImage, Likes, Favorite
from .permissions import IsAuthorOrAdmin
from .serializers import ProductSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'description')
    filterset_fields = ('owner', 'category')

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('q')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(
                description__icontains=search_query)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list', 'toggle_like', 'toggle_favorites'):
            return [permissions.AllowAny(), ]
        elif self.action == 'destroy':
            return [permissions.IsAdminUser(), ]
        return [IsAuthorOrAdmin(), ]

    @action(detail=True, methods=['GET'])
    def toggle_like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = Likes.objects.get_or_create(product=product, user=user)

        like_obj.is_liked = not like_obj.is_liked
        like_obj.save()
        return Response('like toggled')

    # api/v1/products/products/id/favorites/
    @action(detail=True, methods=['GET'])
    def toggle_favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = Favorite.objects.get_or_create(product=product, user=user)

        fav.favorite = not fav.favorite
        fav.save()
        return Response('favourite toggled')

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('likes_from', openapi.IN_QUERY, 'filter products by amount of likes', True,
                          type=openapi.TYPE_INTEGER)])
    @action(detail=False, methods=["GET"])
    def likes(self, request, pk=None):
        from django.db.models import Count
        q = request.query_params.get("likes_from")  # request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.annotate(Count('likes')).filter(likes__count__gte=q)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request}