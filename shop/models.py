import uuid

from django.conf import settings
from django.db import models


CATEGORY_CHOICES = (
    ('', ''),
    ('Mushroom Kits', 'Mushroom Kits'),
    ('Mushroom Powder', 'Mushroom Powder'),
)

TAG_CHOICES = (
    ('', ''),
    ('Featured', 'Featured'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Autumn', 'Autumn'),
    ('Winter', 'Winter'),
)

STATUS_CHOICES = (
    ('Order Created', 'Order Created'),
    ('Order Processing', 'Order Processing'),
    ('Order Ready', 'Order Ready'),
    ('Order Delivered', 'Order Delivered'),
)

CHECKOUT_CHOICES = (
    ('Guest', 'Guest'),
    ('Registered', 'Registered'),
    ('Registered-OTF', 'Registered-OTF'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_type = models.CharField(max_length=20,
                                    choices=CHECKOUT_CHOICES, default='Guest', null=True)
    order_status = models.CharField(max_length=20,
                                    choices=STATUS_CHOICES, default='Order Created', null=True)
    order_id = models.CharField(max_length=120, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    price = models.FloatField(blank=True, default=0)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    first_name = models.CharField(
        max_length=25)
    last_name = models.CharField(
        max_length=25)
    email = models.EmailField(
        max_length=50)
    address_id = models.CharField(max_length=120, blank=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.IntegerField()

    def __str__(self):
        return f'{self.id} {self.item}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def _generate_order_id(self):
        # Generate a random, unique order number using UUID

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):

        # Override the original save method to set the order number
        # if it hasn't been set already.

        if not self.order_id:
            self.order_id = self._generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class Item(models.Model):
    """ Product Model """
    title = models.CharField(max_length=100)  # included in FE > Products.js
    description = models.TextField()  # included in FE > Products.js
    price = models.FloatField()  # included in FE > Products.js
    comparePrice = models.FloatField()  # included in FE > Products.js
    uploadedImg = models.ImageField()  # included in FE > Products.js
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=20, blank=True, null=True)
    tag = models.CharField(choices=TAG_CHOICES,
                           max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES, default='Order Created', null=True)


def __str__(self):
    return f'{self.id} {self.title}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, related_name='items')
    item_id = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True, related_name='orders')
    price = models.FloatField()
    qty = models.IntegerField()
    total = models.FloatField(default=0)
