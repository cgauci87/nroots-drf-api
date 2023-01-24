from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

# AccountManager Model for user and admin 
class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **kwargs):

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")

        if not email:
            raise ValueError("Email is required")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return

# Account Model
class Account(AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reset_password_token = models.CharField(
        max_length=100, null=True, blank=True)

    objects = AccountManager() # Reference to the objects of the Account Manager (see above)

    USERNAME_FIELD = "email" # The email field is being used as the unique identifier

    def has_perm(self, perm, obj=None): # Returns True if the user has the named permission.  If obj is provided, the permission needs to be checked against a specific object instance.
        return True

    def has_module_perms(self, app_label): # Returns True if the user has permission to access models in the given app.
        return True


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="profile")
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    default = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'street_address',
                           'apartment_address', 'city']

    def __str__(self):
        return self.user.email
