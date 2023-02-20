from django.urls import path
from .views import (
    StatusesView,
    CategoriesView,
    TagsView,
    ContactView,
)

app_name = 'shop'

urlpatterns = [

    path('statuses/', StatusesView.as_view(), name='statuses'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('tags/', TagsView.as_view(), name='tags'),
    path("contact", ContactView.as_view(), name="contact"),
]
