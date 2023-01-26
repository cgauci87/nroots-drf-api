from django.http.response import HttpResponse
import json
from django.views.generic import View
from shop.models import CATEGORY_CHOICES, TAG_CHOICES, STATUS_CHOICES

# CategoriesView for CATEGORY_CHOICES
class CategoriesView(View):
    def get(self, *args, **kwargs):
        categories = []
        for c in CATEGORY_CHOICES:
            categories.append(c)

        payload = {'categories': categories}
        return HttpResponse(json.dumps(payload), content_type='application/json')


class TagsView(View):
    def get(self, *args, **kwargs):
        tags = []
        for t in TAG_CHOICES:
            tags.append(t)

        payload = {'tags': tags}
        return HttpResponse(json.dumps(payload), content_type='application/json')


class StatusesView(View):
    def get(self, *args, **kwargs):
        statuses = []
        for s in STATUS_CHOICES:
            statuses.append(s)

        payload = {'statuses': statuses}
        return HttpResponse(json.dumps(payload), content_type='application/json')
