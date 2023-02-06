from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from shop.serializers import ProductSerializer, OrderSerializer
from shop.models import (
    Item,
    Order
)
import django_filters.rest_framework
from rest_framework import filters
from users.permissions import IsAdminOrReadOnly, IsMyOrderOrReadOnly

# ProductViewSet for Item model


class ProductViewSet(ModelViewSet):
    # list, get, update/patch, delete
    model = Item
    serializer_class = ProductSerializer
    # order by created_at (recent created products will display first in the list)
    queryset = Item.objects.all().order_by("-created_at")
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tag']
    search_fields = ['title', 'category']
    ordering_fields = ['price', 'name', 'created_at']


    # using the action decorator with the detail flagged as False to return a list of objects
    @action(detail=False, methods=['DELETE'], permission_classes=[permissions.IsAdminUser])
    def bulk_delete(self, request):
        ids = request.data
        # bulk deletion of multiple products
        Item.objects.filter(pk__in=ids).delete()
        return Response(status=200)


# OrderViewSet for Model Order
class OrderViewSet(ModelViewSet):
    # list, get, update/patch, delete
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsMyOrderOrReadOnly]

    def list(self, request, *args, **kwargs):
        # order by created_at (recent created orders will display first in the list)
        queryset = Order.objects.all().order_by("-created_at")
        # return a list
        return Response(OrderSerializer(queryset, many=True).data)
