from django.http.response import HttpResponse
from rest_framework.response import Response
import json
from django.views.generic import View
from rest_framework.views import APIView
from shop.serializers import ContactSerializer


from django.core.mail import send_mail
from nroots_drf_api.settings import (
    DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
)
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# CategoriesView for CATEGORY_CHOICES


class CategoriesView(View):
    def get(self, *args, **kwargs):
        categories = []
        for c in CATEGORY_CHOICES:
            categories.append(c)

        payload = {'categories': categories}
        # return the payload according to what values specified in the CATEGORY_CHOICES
        return HttpResponse(json.dumps(payload), content_type='application/json')

# TagsView for TAG_CHOICES


class TagsView(View):
    def get(self, *args, **kwargs):
        tags = []
        for t in TAG_CHOICES:
            tags.append(t)

        payload = {'tags': tags}
        # return the payload according to what values specified in the TAG_CHOICES
        return HttpResponse(json.dumps(payload), content_type='application/json')

# StatusesView for STATUS_CHOICES


class StatusesView(View):
    def get(self, *args, **kwargs):
        statuses = []
        for s in STATUS_CHOICES:
            statuses.append(s)

        payload = {'statuses': statuses}
        # return the payload according to what values specified in the STATUS_CHOICES
        return HttpResponse(json.dumps(payload), content_type='application/json')


class ContactView(APIView):
    # post - when user submits contact us form - an email will be send with form contents to the user
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializers.errors, status=400)

        html_message = render_to_string(
            'contact_form.html', {'data': serializer.validated_data})  # loads the template
        # strip/remove HTML tags from an existing string
        plain_message = strip_tags(html_message)
        recipient_list = [data.email, EMAIL_HOST_USER]

        try:
            mail.send_mail("nRoots - Thank you for contacting us", plain_message, EMAIL_HOST_USER,
                            recipient_list, html_message=html_message)  # loads the text file which contain the subject line
        except Exception as e:
            print(e)  # print exception if email delivery not successful
        return Response(status=200)
