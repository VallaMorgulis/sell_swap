from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


class CreateOrderView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly, ]

    # @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:  # Проверка, является ли пользователь администратором
            orders = Order.objects.all()
        else:
            orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)