from django.urls import path
from .views import (
    CategoriesView,
    TagsView,
    ContactView,
)

app_name = 'shop'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('tags/', TagsView.as_view(), name='tags'),
    path("contact", ContactView.as_view(), name="contact"),
]
