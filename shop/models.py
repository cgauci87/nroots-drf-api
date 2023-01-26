import uuid
from django.db import models


CATEGORY_CHOICES = (
    ('Mushroom Kits', 'Mushroom Kits'),
    ('Mushroom Powder', 'Mushroom Powder'),
)

TAG_CHOICES = (
    ('Featured', 'Featured'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Autumn', 'Autumn'),
    ('Winter', 'Winter'),
)

STATUS_CHOICES = (
    # 'Order Created' status would be set automatically once order has been submitted through the checkout
    ('Order Created', 'Order Created'),
    # Status would be updated manually to 'Order Processing' by Admin in CMS
    ('Order Processing', 'Order Processing'),
    # Status would be updated manually to 'Order Ready' by Admin in CMS
    ('Order Ready', 'Order Ready'),
    # Status would be updated manually to 'Order Delivery' by Admin in CMS
    ('Order Delivered', 'Order Delivered'),
)

CHECKOUT_CHOICES = (
    ('Guest', 'Guest'),
    ('Registered', 'Registered'),
    ('Registered-OTF', 'Registered-OTF')
)

ADDRESS_CHOICES = (
    # included Billing choice for future implementation, payment gateway integration
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

# Order Model - used in the checkout process and to manage orders in CMS


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_type = models.CharField(max_length=20,
                                     choices=CHECKOUT_CHOICES, default='Guest', null=True)  # including CHECKOUT_CHOICES
    order_status = models.CharField(max_length=20,
                                    choices=STATUS_CHOICES, default='Order Created', null=True)  # including STATUS_CHOICES
    # Generate a random id, unique order number using UUID (see below def)
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
    address_type = models.CharField(
        max_length=1, default='S', choices=ADDRESS_CHOICES)  # including ADDRESS_CHOICES
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.IntegerField()

    def __str__(self):
        # generate string representations of the objects
        return f'{self.id} {self.item}'

    # this decorator declare that it can be accessed like it's a regular property.
    @property
    def full_name(self):  # returns a string with the user first and last name.
        return f'{self.first_name} {self.last_name}'

    def generate_order_id(self):
        # generate a random, unique order number using UUID

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):

        # Override the original save method to set the order number
        # if it hasn't been set already.

        if not self.order_id:
            self.order_id = self.generate_order_id()
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
