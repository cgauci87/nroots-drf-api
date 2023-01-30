from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.
from cms.tests import CommonTest

class UserTest(CommonTest):
    
    def get_register_data(self, first_name='test', last_name='fakename', email='test@test.com', password='Testing123@', password2=None):
        if not password2:
            password2 = password
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'password2': password2
        }
    
    def test_user_register_success(self):
        
        data = self.get_register_data()
        self.assertFalse(self.unauth_client.login(username=data['email'],password=data['password']))
        
        response = self.unauth_client.post('/auth/register', data)
        self.assertEquals(response.status_code, 200)
        
        self.assertTrue(self.unauth_client.login(username=data['email'], password=data['password']))
        
    def test_user_register_fail_incorrect_password2(self):
        
        data = self.get_register_data(password2='12313123321')
        self.assertFalse(self.unauth_client.login(username=data['email'],password=data['password']))
        response = self.unauth_client.post('/auth/register', data)
        self.assertFalse(self.unauth_client.login(username=data['email'],password=data['password']))
        self.assertEquals(response.status_code, 400)
        
    def test_user_login_success(self):
        data = {'email': 'johndoe@example.com', 'password': 'pass'}
        response = self.unauth_client.post('/auth/login', data)
        self.assertEquals(response.status_code, 200)

    def test_user_login_fail_incorrect_pass(self):
        data = {'email': 'johndoe@example.com', 'password': 'pass123'}
        response = self.unauth_client.post('/auth/login', data)
        self.assertEquals(response.status_code, 401)
        
    def test_user_login_fail_user_inactive(self):
        inactive_user = User.objects.create_user(
            first_name='john', last_name='doe', email='inactive@example.com', password='pass')
        inactive_user.is_active = False
        inactive_user.save()
        data = {'email': inactive_user.email, 'password': 'pass'}
        response = self.unauth_client.post('/auth/login', data)
        print(response.content)
        self.assertEquals(response.status_code, 401)
        