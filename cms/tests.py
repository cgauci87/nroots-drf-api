from django.conf import settings
from shop.models import (
    Item,
    Order
)

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            first_name='john', last_name='doe', email='johndoe@example.com', password='pass', is_staff=True, is_admin=True)
        User.objects.create_user(
            first_name='john', last_name='doe', email='regular@example.com', password='pass')
        user = self.client.login(email='johndoe@example.com', password='pass')
        user = User.objects.get(email='johndoe@example.com')
        user.is_staff = True
        user.save()
        self.unauth_client = APIClient()
        self.regular_client = APIClient()
        self.regular_client.login(email='regular@example.com', password='pass')
    
    def get_order_data(self):
        return {'items': [{
            
            'item_id': self.product_1.id,
            'qty': 1
            }],
            'first_name': 'Billy',
            'last_name': "Fakename",
            'email': 'test@test.com',
            'apartment_address': '1',
            'street_address': '1',
            'city': 'Some city',
            'phone_number': '5555555555',
        }


class ProductListViewSetTests(CommonTest):
    """Product List View Set Tests"""

    def test_anonymous_user_can_list_items_in_shop(self):
        """Test that an anonymous user can list all items in the shop"""
        response = self.unauth_client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_authenticated_user_can_list_items_in_shop(self):
        """Test that an authenticated user can list all items in the shop"""
        
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_admin_user_can_list_items_in_shop(self):
        """Test that an admin user can list all items in the shop"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class ProductDetailViewSetTests(CommonTest):
    """Product Detail View Set Tests"""

    def setUp(self):
        super().setUp()
        self.product_1 = Item.objects.create(
            title='product title one', description='product description one'
        )
        self.product_2 = Item.objects.create(
            title='product title two', description='product description two'
        )

    def test_can_retrieve_item_using_valid_id(self):
        """Test that a user can retrieve a post using a valid ID"""
        response = self.client.get(f'/products/{self.product_1.pk}/')
        self.assertEqual(response.data['title'], self.product_1.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_item_using_invalid_id(self):
        """Test that a user can't retrieve a post using an invalid ID"""
        response = self.client.get('/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_cant_post_to_add_product(self):
        """Test that a user can't post a product"""

        response = self.regular_client.post('/products/', {
            'title': 'a new title',
            'description': 'desc',
            'price': 999,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   

    def test_anonymous_user_can_submit_order(self):
        """Test that an anonymous user can submit an order """
        response = self.client.post('/order/', self.get_order_data(), format='json')
        count = Order.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_submit_order_and_save_shipping_address(self):
        """Test that an authenticated user can submit an order and save shipping address """
        data = self.get_order_data()
        
        self.assertEquals(Order.objects.filter().count(), 0)
        response = self.client.post('/order/', data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Order.objects.filter().count(), 1)

    def test_admin_user_can_submit_order(self):

        response = self.client.post('/order/', self.get_order_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        count = Order.objects.count()
        self.assertEqual(count, 1)
        
    def test_delete_bulk_product_success(self):
        items = Item.objects.all()
        num_products = items.count()
        self.assertNotEqual(num_products, 0)
        ids = [x.id for x in items]
        response = self.client.delete('/products/bulk_delete/', ids, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.all().count(), 0)