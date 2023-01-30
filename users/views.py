
import uuid
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from django.http import JsonResponse
from rest_framework.response import Response

from django.core.mail import send_mail
from nroots_drf_api.settings import (
    DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
)
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from users import serializers, models
from users.models import Address
from users.serializers import AddressSerializer

# Get user tokens - refresh_token & access_token


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

# User authentication by email


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # Perform validation

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)
    allow_login = user and user.is_active
    if allow_login:
        tokens = get_user_tokens(user)
        res = response.Response()
        # Set cookies upon successful response
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    # raise exception if user has entered incorrect email address or incorrect password or both
    raise rest_exceptions.AuthenticationFailed(
        "Email or Password is incorrect!")

# User Registration by email


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    #  deserializing data - call is_valid() before attempting to access the validated data
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    # Success message if response is successful
    response = {'message': 'Account created successfully',
                'user': serializers.AccountSerializer(user).data}
    if user is not None:
        return JsonResponse(response)
    # return exception if failed
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

# Logout function - remove token cookies


@rest_decorators.api_view(['GET'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:  # get token cookies
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()
        # delete token cookies upon successful response on logout
        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"] = None

        return res
    except:  # if token not found or doesn't match , raise parse error exception
        raise rest_exceptions.ParseError("Invalid token")

# Cookie Token Refresh Serializer


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None
    # Validation - get refresh cookie and validate

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')

# Cookie Token Refresh View


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer
    # If response would have the refresh object -  set values so to "refresh" the access token.

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)

# userView for Account Model


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def userView(request):
    try:  # Get objects from the account of current logged in user
        user = models.Account.objects.get(id=request.user.id)
    except models.Account.DoesNotExist:
        # if account does not exists, then raise exception 404
        return response.Response(status_code=404)
        #
    serializer = serializers.AccountSerializer(user)
    # if response is successful, return serialized data
    return response.Response(serializer.data)

# userProfileView for Account Model


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticatedOrReadOnly])
def userProfileView(request):
    try:  # Get objects from the account of current logged in user
        user = models.Account.objects.get(id=request.user.id)
    except models.Account.DoesNotExist:
        # if account does not exists, then raise exception 404
        return response.Response(status_code=404)
     # if response is successful, return serialized data
    serializer = serializers.AccountSerializer(user)
    return response.Response(serializer.data)

# ForgotPassword - API View
class ForgotPassword(APIView):
    def post(self, request, *args, **kwargs): #post - when user input his email address and hit submit to initiate the forgot password reset process
        FRONTEND_URL = "https://nroots-react.herokuapp.com"
        user = models.Account.objects.filter(
            email=request.data.get("email")).first() # get email from the input of the user
        if user:
            token = str(uuid.uuid4().hex) # generate token with uuid
            token = token.replace("=", "").replace("&", "")

            user.reset_password_token = token # set the token
            user.save()
            url = FRONTEND_URL + "/auth/reset-password?reset_token=" + token # parse the url with the reset_token

            html_message = render_to_string(
                'reset_password.html', {'url': url}) # loads the template
            plain_message = strip_tags(html_message) # strip/remove HTML tags from an existing string

            try:
                mail.send_mail("NRoots - Reset Your Account Password", plain_message, EMAIL_HOST_USER, [
                               user.email], html_message=html_message) # loads the text file which contain the subject line
            except Exception as e:
                print(e) # print exception if email delivery not successful

            print(url)
            response = {
                'message': 'A password link has been sent to the registered email'}
        return JsonResponse(response) # return success response if successful

    def patch(self, request, *args, **kwargs): #patch - when user receieve the forgot password email and proceed to reset the password via the link with token that was provided.
        if not "reset_token" in request.data:
            return response.Response(status_code=404)
        user = models.Account.objects.filter(
            reset_password_token=request.data.get("reset_token")).first() # Get the reset token from the url
        if not user:
            response.Response(status_code=404) # return exception if user invalid
        if user:
            # reset the token to a random value so to expire it
            user.reset_password_token = str(uuid.uuid4().hex)
            # set the new password
            user.set_password(request.data.get("confirm_password"))
            # save the new password
            user.save()
            # success response
            response = {'message': 'Your new password has been set.'} # success message if response is successful
        else:
            response = {'message': 'User not found'} # pending bug
        return JsonResponse(response)


class ChangeCurrentPasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data.get("password")):
            return self.send_response(
                success=False,
                message=ResponseMessages.INVALID_PASSWORD,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if not request.data.get("new_password") == request.data.get("confirm_password"):
            return self.send_response(
                success=False,
                message=ResponseMessages.PASSWORD_MISMATCH,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        user.set_password(request.data.get("new_password"))
        user.save()
        return self.send_success_response(message="Success")

# AddressViewSet for Model Address
class AddressViewSet(ModelViewSet):
    # list, get, update/patch, delete
    model = Address
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

    def query_set(self, request, *args, **kwargs):
        user = User.objects.filter(email=current_user.email) # filter by current user email object
        queryset = Address.objects.filter(user=self.request.user) # query only the address objects of the current user
        serializer = AddressSerializer(queryset, many=True) # a nested representation of list of items
        return Response(serializer.data) # return response from serialized data
