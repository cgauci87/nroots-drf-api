from django.contrib import admin
from users.models import Account, Address
from shop.models import Item, Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.admin import \
    OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class AccountAdmin(UserAdmin):
    filter_horizontal = []
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    
    add_fieldsets = (
        (
            None, {
                'fields': ['email', 'password1', 'password2']
            },
        ),
    )

    fieldsets = (
        ('User Information', {'fields': ('email', 'first_name', 'last_name',
                                         'is_superuser', 'is_admin',
                                         'is_staff', 'is_active',
                                         'reset_password_token',
                                         'password')},),)

class OrderItemInline(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Account, AccountAdmin)
admin.site.register(Address)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
