from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from shop.serializers import ProductSerializer, OrderSerializer
from shop.models import (
    Item,
    Order
)


class ProductViewSet(ModelViewSet):
    # list, get, update/patch, delete
    model = Item
    serializer_class = ProductSerializer
    queryset = Item.objects.all()
    # permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def products(self, request, *args, **kwargs):
        queryset = Item.objects.all().order_by("-created_at")
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = Item.objects.all().order_by("-created_at") # pending bug
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=['DELETE'])
    def bulk_delete(self, request):
        ids = request.data

        Item.objects.filter(pk__in=ids).delete()
        return Response(status=200)


# @user_passes_test(Account.is_admin)
class OrderViewSet(ModelViewSet):
    # list, get, update/patch, delete
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.all().order_by("-created_at")
        return Response(OrderSerializer(queryset, many=True).data)
