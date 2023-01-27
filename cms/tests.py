from django.conf import settings
from shop.models import (
    Item,
    Order
)

from rest_framework import status
from rest_framework.test import APITestCase


class ProductListViewSetTests(APITestCase):
    """Product List View Set Tests"""

    def setUp(self):
        User.objects.create_user(
            first_name='john', last_name='doe', email='johndoe@example.com', password='pass')

    def test_anonymous_user_can_list_items_in_shop(self):
        """Test that an anonymous user can list all items in the shop"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_authenticated_user_can_list_items_in_shop(self):
        """Test that an authenticated user can list all items in the shop"""
        self.client.login(email='johndoe@example.com', password='pass')
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_admin_user_can_list_items_in_shop(self):
        """Test that an admin user can list all items in the shop"""
        self.client.login(email='admin@example.com',
                          password='pass', is_admin='True')
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class ProductDetailViewSetTests(APITestCase):
    """Product Detail View Set Tests"""

    def setUp(self):
        john = User.objects.create_user(username='john', password='pass')
        sarah = User.objects.create_user(username='sarah', password='pass')
        Item.objects.create(
            title='product title one', description='product description one'
        )
        Item.objects.create(
            title='product title two', description='product description two'
        )

    def test_can_retrieve_item_using_valid_id(self):
        """Test that a user can retrieve a post using a valid ID"""
        response = self.client.get('/products/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_item_using_invalid_id(self):
        """Test that a user can't retrieve a post using an invalid ID"""
        response = self.client.get('/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_can_submit_order(self):
        """Test that an anonymous user can submit an order """
        response = self.client.post('/order/', {'title': 'a product title'})
        count = Order.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_submit_order_and_save_shipping_address(self):
        """Test that an authenticated user can submit an order and save shipping address """
        self.client.login(email='johndoe@example.com', password='pass')
        response = self.client.post('/order/', {'title': 'a product title'})
        count = Order.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test__admin_user_can_submit_order(self):
        """Test that an admin can submit an order  """
        self.client.login(email='johndoe@example.com', password='pass')
        response = self.client.post('/order/', {'title': 'a product title'})
        count = Order.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
