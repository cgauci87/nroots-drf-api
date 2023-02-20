from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class AccountAdmin(UserAdmin):
    filter_horizontal = []
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']

    fieldsets = (
        ('User Information', {'fields': ('email', 'first_name', 'last_name', 'is_superuser', 'is_admin', 'is_staff', 'is_active', 'reset_password_token', 'password')},
         ),
    )


admin.site.register(Account, AccountAdmin)

class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
