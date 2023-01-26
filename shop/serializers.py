from rest_framework import serializers
from shop.models import Item, Order, OrderItem

from django.core.mail import send_mail
from mycoapp.settings import (
    DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
)
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import *



# Base64ImageField Serializer - decode image file - mainly used to upload product images

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
             # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]  # set 12 characters
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file): # check file extension
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

# ProductSerializer for Item model using DecimalField for pricing/total to avoid precision issues
class ProductSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comparePrice = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    uploadedImg = Base64ImageField() # an image representation for Base64ImageField, inherited from ImageField
    created_at = serializers.DateTimeField(
        format='%d/%m/%y %H:%M', required=False) # timstamp in human readable format

    class Meta:
        model = Item
        fields = '__all__'

# OrderItemSerializer for OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(default=0.00, max_digits=10, decimal_places=2) # using DecimalField for total to avoid precision issues
    title = serializers.CharField(source='item_id.title', read_only=True) # specified a source parameter

    class Meta:
        model = OrderItem
        fields = ['item_id', 'price', 'qty', 'total', 'title']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, required=False)
    checkout_type = serializers.CharField(required=False)

    created_at = serializers.DateTimeField(
        format='%d/%m/%y %H:%M', required=False)

    full_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = super().create(validated_data)
        qty = 0
        total = Decimal(0)

        for item_id in items:
            item_id['item_id'] = item_id['item_id'].pk

            item_id = OrderItemSerializer(data=item_id)
            if not item_id.is_valid():
                print(item_id.errors)
                raise serializers.ValidationError("Invalid item")
            item_id = item_id.save()
            item_id.order = order
            item_id.total = item_id.price * item_id.qty
            item_id.save()
            total += item_id.total
            qty += item_id.qty
        order.qty = qty
        order.price = total
        order.save()

        # SEND ORDER SUMMARY EMAIL HERE

        html_message = render_to_string('order_summary.html', {'order': order})
        plain_message = strip_tags(html_message)
        subject = render_to_string(
            'order_summary_subject.txt',
            {'order': order})

        try:
            mail.send_mail(subject, plain_message, EMAIL_HOST_USER, [
                order.email], html_message=html_message)
        except Exception as e:
            print(e)

        return order

    class Meta:
        model = Order
        fields = '__all__'
