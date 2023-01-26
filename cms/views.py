from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from shop.serializers import ProductSerializer, OrderSerializer
from shop.models import (
    Item,
    Order
)

# ProductViewSet for Item model


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

    # def list(self, request, *args, **kwargs): # pending bug
    #     queryset = Item.objects.all().order_by("-created_at") # order by created_at (recent created products will display first in the list)
    #     serializer = ProductSerializer(queryset, many=True) # a nested representation of list of items
    #     return Response(serializer.data) # return serialized data

    # using the action decorator with the detail flagged as False to return a list of objects
    @action(detail=False, methods=['DELETE'])
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

    def list(self, request, *args, **kwargs):
        # order by created_at (recent created products will display first in the list)
        queryset = Order.objects.all().order_by("-created_at")
        # return a list
        return Response(OrderSerializer(queryset, many=True).data)
