# Table of Contents

1. [Introduction](#introduction)
2. [Database Schema](#database-schema---entity-relationship-diagram)
3. [Testing](#testing)
4. [Bugs](#bugs)
    1. [Fixed](#fixed)
    2. [Unfixed](#unfixed)
5. [Technologies Used](#technologies-used)
     1. [Modules](#modules)
     2. [Languages](#languages)
     3. [Libraries](#libraries)
     4. [Frameworks](#frameworks)
     5. [Platforms](#platforms)
     6. [Services](#services)
     7. [Resources](#resources)
6. [Project Setup](#project-setup)
7. [Deployment](#deployment)
    1. [Set up Simple JWT](#set-up-simplejwt-steps-1-12)
    2. [Prepare API for deployment to Heroku](#prepare-api-for-deployment-to-heroku-steps-13-18)
    3. [Deploy to Heroku](#deploy-to-heroku-steps-19-43)
8. [Django Templates](#django-templates)
9. [Credits](#credits)
10. [Media](#media)

***

# Introduction

nRoots is a Shop for house plant lovers with CMS pages (Content Management System) inclusive and restricted for Admin or is_staff. Admin/is_staff can add, edit products and view orders.
Users (shoppers) can register for an account - Either by sign up through the standard registration form or during the checkout process; registration on the fly.
By having an account - registered users would have their shipping address/es being saved automatically upon order submission. This is a time saving feature for registered returning customers.
No duplicate addresses would be saved. Registered user can find their saved addresses either from their account section or in the checkout page. 
Guest users would still be able to add/remove items to shopping cart and proceed with checkout. However shipping address won't be saved upon order submission.

This repository holds the Django Rest Framework (DRF) API database for the ReactJS frontend part of the project. 

[Deployed DRF API (via Render)]()

[Deployed Front End]()

[Front End README.md]()

[Front End TESTS.md]()


***

# Database Schema - Entity Relationship Diagram

![Entity Relationship Diagram]()

***

# Testing
- All testing documentation can be found [here]()

***

# Bugs

## Fixed

- When attempting to add a product image, I encountered the following error: "In order to use cloudinary storage, you need to provide CLOUDINARY_STORAGE dictionary with CLOUD_NAME, API_SECRET and API_KEY in the settings or set CLOUDINARY_URL variable (or CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET variables)".
This error was showing because the env.py file was not saved in the correct file structure. Upon moving the file to the root directory, this error was rectified. 

- At the initial stage of this project, I used FloatField to represent pricing in the model. However, FloatField uses the float type 
internally which comes with some precision issues. I decided to replace it with DecimalField , however I encountred a bug upon an order submission.
Django backend got an error "unsupported operand type(s) for *: 'float' and 'Decimal'".
To solve this issue, I imported Decimal and defined the problematic field, in this case "Total" as "Decimal(0)" 

## Unfixed

None identified

***

# Technologies Used

## Modules

![Modules used](static/readme_images/modules_used.png)

## Languages
- Python - The base language of the Django REST Framework

## Libraries
- Django Rest Framework SimpleJWT
- Django Cloudinary Storage
- Django Filter
- PostgreSQL
- Cors Headers

## Frameworks
- Django REST Framework

## Platforms
- Cloudinary - Storage of image files
- Github - Repository with Git version control
- GitPod - IDE used for development
- Heroku - Hosting of DRF database

## Services 

- [DrawSQLapp](https://drawsql.app/) - Development of database schema

## Resources
- The Code Institute's DRF walkthrough was used as a guide on how to set up, build and deploy a DRF API. I customised existing models and created new ones as my confidence and knowledge grew. 
- The Code Institute DRF Cheat Sheet was used as a reference guide, particularly for specific terminal commands.
- Django Rest Framework documentation was relied on for additional functionality.
- W3C Schools and Stack Overflow were used for general enquiries relating to Django Rest Framework. 

***

# Project Setup

1. Create a new repository from the Code Institute template repository.
2. Run terminal command **pip3 install 'django<4'** to install Django.
3. Run terminal command **django-admin startproject nroots_drf_api .** (make sure to include the dot at the end to initialize project in it's current directory).
4. Run terminal command **pip install django-cloudinary-storage** to install Django Cloudinary Storage.
5. Add the newly installed apps 'cloudinary_storage' and 'cloudinary' to INSTALLED_APPS in settings.py as shown below:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage', 
    'django.contrib.staticfiles',
    'cloudinary',
]
```
6. Create env.py in the root directory, import os and add the CLOUDINARY_URL as shown below: 

```
import os
os.environ["CLOUDINARY_URL"] = "cloudinary://API KEY HERE"
```
7. Back in settings.py, load environment variable with Cloudinary credentials, set a CLOUDINARY_STORAGE variable, define the MEDIA_URL folder and set a DEFAULT_FILE_STORAGE variable as follows:

```
import os

if os.path.exists('env.py'):
    import env

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

***

# Deployment

## Set up Simple JWT (steps 1-12)

1. Firstly, to install Simple JWT Authentication run terminal command **pip install djangorestframework-simplejwt**

2. Add  'rest_framework_simplejwt.token_blacklist' to the list of INSTALLED_APPS in settings.py

3. Add Simple JWT's settings variables as below: 
```
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    # custom
    'AUTH_COOKIE': 'access',
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh',
    # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_DOMAIN': None,
    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': True,
    # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
    # can be modified to Lax if CORS_ORIGIN_WHITELIST has both BE & FE urls - otherwise set to None
    'AUTH_COOKIE_SAMESITE': "None",
}
```
4. Create a custom user model and then migrate the database with terminal command **python manage.py migrate**

5. Create serializers.py in users app

6. Create views for registering the user and login

7. Define URL for Views

8. Add the auth urls below to the main urls.py file: 
```
 path('auth/', include("users.urls", namespace='users')),
```

9. Add the following to settings.py: 
```
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',],


TESTING = sys.argv[1:2] == ['test']

if TESTING:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'rest_framework.authentication.SessionAuthentication')



AUTH_USER_MODEL = "users.Account"
```

10. Migrate the database again with terminal command **python manage.py migrate**

11. Update requirements.txt file with new dependencies by running terminal command **pip freeze > requirements.txt**

12. Add, commit and push changes. 




## Prepare API for deployment to Heroku (steps 13-18)

13. To add a custom message to the root_route, create a views.py file in the drf_api directory and add the following code:

```
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to nRoots DRF API!"
    })
```

14. Import to the main urls.py file, and add to the top of the urlpatterns list as follows: 

```
from .views import root_route

urlpatterns = [
    path('', root_route),
```

15. To set up page pagination and date/time format, add the following to settings.py (inside REST_FRAMEWORK):
```
    "DEFAULT_PAGINATION_CLASS":
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
```

16. To set up default permission classes, add the following to settings.py (inside REST_FRAMEWORK):
```
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
    ],
```

17. For filtering data in Django:

run terminal command **pip install django-filter**

and add the following to settings.py:

```
INSTALLED_APPS = [
    .......
    'django_filters'
]
```

18. Add, commit and push changes 

## Deploy to Heroku (steps 19-43 )

19. Log into Heroku and create a new app. 

20. Go to 'Resources' to search for Heroku Postgres in the Add-Ons section and select plan.

21. Go to 'Settings' and click on 'Reveal Config Vars' to confirm DATABASE_URL is present. 

22. Go back to Git workspace and run terminal command **pip install dj_database_url psycopg2** to install the relevant libraries needed to use a Heroku postgres database. 

23. Import dj_database_url to settings.py:
```
import dj_database_url
```

24. Go to DATABASES in settings.py and separate development and production environments. Also, set DEBUG as follows: 
```
if os.environ.get('DEVELOPMENT') == "True":
    # Testing database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    DEBUG = True
else:
    # Heroku database PRODUCTION
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
    }

    DEBUG = False  # PRODUCTION
```

25. Install Gunicorn library by running terminal command **pip install gunicorn**

26. Add a Procfile to the top level of the directory and add the following code to the file: 
```
release: python manage.py makemigrations && python manage.py migrate
web: gunicorn drf_api.wsgi
```

27. Set ALLOWED_HOSTS in settings.py: 
```
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST'),
    'localhost',
]
```

28. Set CORS_ALLOWED_ORIGINS in settings.py: 
```
CORS_ALLOWED_ORIGINS = [
    os.environ.get('CORS_ALLOWED_ORIGINS')
]
```

29. Set CSRF_TRUSTED_ORIGINS in settings.py: 
```
CSRF_TRUSTED_ORIGINS = [
    os.environ.get('CSRF_TRUSTED_ORIGINS')
]
```

30. Install Cors Headers library by running terminal command **pip install django-cors-headers**

31. Add 'corsheaders' to INSTALLED_APPS list in settings.py

32. Add to the top of the MIDDLEWARE list in settings.py as follows: 
```
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

33. Add CSRF settings and session cookie variables as follows: 
```
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CSRF_TRUSTED_ORIGINS = [
    os.environ.get('CSRF_TRUSTED_ORIGINS')]
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = True
```

34. In settings.py, set SECRET_KEY variable as follows:
```
SECRET_KEY = os.environ.get('SECRET_KEY')
```

35. Copy the CLOUDINARY_URL and SECRET_KEY values from env.py and add them to Heroku config vars. 

36. Add config var COLLECT_STATIC and set to 1. 

37. Update requirements.txt file with new dependencies by running terminal command **pip freeze > requirements.txt**

38. Add, commit and push changes.

39. Go back to Heroku and click on 'Deploy'. Go to 'Deployment Method' and click on GitHub. 

40. Connect to the DRF repository. 

41. In 'Manual Deploy' select Main branch and click 'Deploy Branch'. 

42 Monitor build log and deployment blog to ensure no error messages display. If build is successful, the app is now deployed. 

43. Click on 'Open app' to access deployed app.

# Django Templates

Template based email notifications have been created, for the following:

- Account creation; This email notification will be send automatically upon a user register an account.
- Forgot password; This email notifications with a link and token will be send automatically upon user request to reset password.
- Order Summary; This email notification will be send automatically upon a user submit an order.
- Contact form; A copy of the message sent via the contact form, will be sent to the admin and the user who submitted the form.

44. In settings.py, add Django Gmail SMTP server configuration: 
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 10
```
then, add the following variables to Heroku: 
```
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

45. Add, commit and push changes. 

46. Return to Heroku and manually deploy again. 

## Adding extra required environment variables - required to use API with Frontend part of project (steps 47-52)

47. In settings.py, add heroku app url to ALLOWED_HOSTS: 
```
ALLOWED_HOSTS = [
    '....herokuapp.com'
    'localhost',
]
```

48. Go to Heroku deployed app, and go to 'Settings' then 'Reveal config vars'. 

49. Add the new ALLOWED_HOST key with the value of your deployed URL (as added to ALLOWED_HOSTS).

50. Go back to settings.py and replace the url string with the ALLOWED_HOST environment variable"
```
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST'),
    'localhost',
]
```
51. Add, commit and push changes. 

52. Return to Heroku and manually deploy branch for a final time. 
 
***

# Credits

- The Code Institute DRF-API walkthrough was used as an invaluable guide on how to build a DRF-API. 
- Team at Tutor Support for their assistance. 
- Fellow students for peer support and chats. 
- Slack Community for an invaluable archive of help! 

***

# Media 

- All media images from [Pexels](https://www.pexels.com/) - free stock images.
