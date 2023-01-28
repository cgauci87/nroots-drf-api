from django.urls import path
from cms.views import ProductViewSet, OrderViewSet
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter # DefaultRouter includes a default API root view

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [] + router.urls # append router.urls to the above list of views.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serving static files
