from django.apps import AppConfig

""" Auto-incrementing Primary Key """


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms'
