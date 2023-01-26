from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views
from users.views import AddressViewSet

app_name = "users"

router = DefaultRouter() # DefaultRouter includes a default API root view
router.register('user/profile/addresses', views.AddressViewSet)

urlpatterns = [
    path('login', views.loginView),
    path('register', views.registerView),
    path('refresh-token', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
    path('user/', views.userView),
    path('user/profile/', views.userProfileView),
    path('forgot-password', views.ForgotPassword.as_view()),
    path('reset-password', views.ChangeCurrentPasswordView.as_view()),
]

urlpatterns += router.urls # append router.urls to the above list of views.
