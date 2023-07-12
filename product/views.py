from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from . import serializers
from .models import Product, ProductImage
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
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]
        elif self.action == 'destroy':
            return [permissions.IsAdminUser(), ]
        return [IsAuthorOrAdmin(), ]

    # api/v1/products/<id>/reviews/
    # @action(['GET', 'POST'], detail=True)
    # def reviews(self, request, pk):
    #     product = self.get_object()
    #     if request.method == 'GET':
    #         reviews = product.reviews.all()
    #         serializer = ReviewActionSerializer(reviews, many=True).data
    #         return response.Response(serializer, status=200)
    #     else:
    #         if product.reviews.filter(owner=request.user).exists():
    #             return response.Response('You already reviewed this product!',
    #                                      status=400)
    #         data = request.data  # rating text
    #         serializer = ReviewActionSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(owner=request.user, product=product)
    #         return response.Response(serializer.data, status=201)

    # api/v1/product/id/
    # @action(['DELETE'], detail=True)
    # def review_delete(self, request, pk):
    #     product = self.get_object()  # Product.objects.get(id=pk)
    #     user = request.user
    #     if not product.reviews.filter(owner=user).exists():
    #         return response.Response('You didn\'t reviewed this product!',
    #                                  status=400)
    #     review = product.reviews.get(owner=user)
    #     review.delete()
    #     return response.Response('Successfully deleted', status=204)
