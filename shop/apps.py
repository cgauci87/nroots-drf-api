from django.apps import AppConfig

""" Auto-incrementing Primary Key """


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
