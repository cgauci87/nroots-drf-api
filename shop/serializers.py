from rest_framework import serializers
from shop.models import Item, Order, OrderItem

from django.core.mail import send_mail
from nroots_drf_api.settings import (
    DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
)
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from decimal import *
from users.models import Address


# Base64ImageField Serializer - decode image file
# mainly used to upload product images

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

    def get_file_extension(self, file_name, decoded_file):  # check extension
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

# ProductSerializer for Item model using DecimalField for pricing/total
# to avoid precision issues


class ProductSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    comparePrice = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    # an image representation for Base64ImageField, inherited from ImageField
    uploadedImg = Base64ImageField()
    created_at = serializers.DateTimeField(
        format='%d/%m/%y %H:%M', required=False)
    # timstamp in human readable format

    class Meta:
        model = Item
        fields = '__all__'

# OrderItemSerializer for OrderItem model


class OrderItemSerializer(serializers.ModelSerializer):
    # using DecimalField for total to avoid precision issues
    total = serializers.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    # specified a source parameter
    title = serializers.CharField(source='item_id.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_id', 'price', 'qty', 'total', 'title']


# OrderSerializer for Order model
class OrderSerializer(serializers.ModelSerializer):

    # a nested representation of list of items
    items = OrderItemSerializer(many=True, required=False)
    checkout_type = serializers.CharField(required=False)

    created_at = serializers.DateTimeField(
        format='%d/%m/%y %H:%M', required=False)
    # timstamp in human readable format

    # visible field, but not editable by the user
    full_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        # .pop searches for 'items' and returns and removes it if it is found,
        # otherwise an exception is thrown.
        items = validated_data.pop('items')
        order = super().create(validated_data)
        qty = 0
        total = Decimal(0)  # create a Decimal from decimal import *

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            Address.objects.get_or_create(
                apartment_address=order.apartment_address,
                street_address=order.street_address,
                city=order.city,
                phone_number=order.phone_number,
                user=user
            )

        # a nested field on the serializer class
        # (writable nested serialization)
        for item_id in items:
            item_id['item_id'] = item_id['item_id'].pk

            item_id = OrderItemSerializer(data=item_id)
            if not item_id.is_valid():
                print(item_id.errors)
                # raise validation error if item_id is not valid
                raise serializers.ValidationError("Invalid item")
            item_id = item_id.save()
            item_id.order = order
            item_id.total = item_id.price * item_id.qty  # calculate total
            item_id.save()
            total += Decimal(item_id.total)
            qty += item_id.qty
        order.qty = qty
        order.price = total
        order.save()  # save order to database

        # SEND ORDER SUMMARY EMAIL HERE
        # (triggered automatically upon order submission)

        html_message = render_to_string(
            'order_summary.html', {'order': order})  # loads the template
        # strip/remove HTML tags from an existing string
        plain_message = strip_tags(html_message)
        subject = render_to_string(
            'order_summary_subject.txt',
            {'order': order})
        # loads the text file which contain the subject line

        try:
            mail.send_mail(subject, plain_message, EMAIL_HOST_USER, [
                order.email], html_message=html_message)
            # Sending email by using the send_mail function (imported).
        except Exception as e:
            print(e)  # print exception if email delivery not successful

        return order

    class Meta:
        model = Order
        fields = '__all__'


# ContactSerializer for Contact us form

class ContactSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
