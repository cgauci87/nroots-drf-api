from rest_framework import serializers
from django.conf import settings
from users.models import Account, Address

from django.core.mail import send_mail
from nroots_drf_api.settings import (
    DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
)
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Registration Serializer for Model Account


class RegistrationSerializer(serializers.ModelSerializer):

    # set the input type on password2 field as password for hidden style
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "password", "password2")
        read_only_fields = ("is_superuser", "is_admin",
                            "is_staff", "is_active", "created_at", "updated_at")  # listing the said fields as read only, this would prevent fields from being changed in an update
        extra_kwargs = {  # Listing password and password2 fields in the additional keyword arguments
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):  # create a new instance.
        user = Account(  # returns the validated incoming data
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:  # if both fields does not match, then raise a validation error
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        # pass to set_password method, creates a hashed password
        user.set_password(password)
        user.save()  # save the value in database

        # SEND ACCOUNT CREATED EMAIL HERE (triggered automatically upon account creation)

        html_message = render_to_string(
            'account_created.html', {'user': user})  # loads the template
        # strip/remove HTML tags from an existing string
        plain_message = strip_tags(html_message)
        subject = render_to_string(
            'account_created_subject.txt',
            {'user': user})  # loads the text file which contain the subject line

        try:
            mail.send_mail(subject, plain_message, EMAIL_HOST_USER, [
                user.email], html_message=html_message)  # Sending email by using the send_mail function (imported).
        except Exception as e:
            print(e)  # print exception if email delivery not successful

        return user

# Login Serializer for Model Account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)  # set the input type on password2 field as password for hidden style


class AccountSerializer(serializers.ModelSerializer):
    # listing the said fields as read only, this would prevent fields from being changed in an update
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "first_name", "last_name",
                  "email", 'is_staff', 'is_active')  # listing the said fields as a subset of the default fields to be used in a model serializer

# Address Serializer for Model Address


class AddressSerializer(serializers.ModelSerializer):
    # specified source parameter for each
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Address
        fields = "__all__"
        validators = [  # enforce unique_together constraints on Address instances to prevent duplicate data on checkout process if same address has already been saved
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'street_address', 'apartment_address', 'city'),
                message=("The address already exists so it won't be saved again")
            )
        ]

    def create(self, validated_data):  # overriding the create() method for Model Address
        validated_data['default'] = True
        inst = super().create(validated_data)

        Address.objects.filter(user_id=inst.user_id).exclude(
            pk=inst.pk).update(default=False)

        # find all address by this user, exclude the one created, set them to false
        # update addresses set default=False WHERE user_id = <user_id> and id <> inst.id
        return inst
