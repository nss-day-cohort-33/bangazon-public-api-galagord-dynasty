"""bangazonAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapp.models import *
from bangazonapp.views import register_user, login_user
from bangazonapp.views import Customers
from bangazonapp.views import CategoryTypes
from bangazonapp.views import Payments
from bangazonapp.views import Products, UserViewSet, Orders, OrderProducts

# pylint: disable=invalid-name

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
router.register(r'categories', CategoryTypes, 'categorytype')
router.register(r'payments', Payments, 'payment')
router.register(r'products', Products, 'product')
router.register(r'users', UserViewSet, 'user')
router.register(r'orders', Orders, 'order')
router.register(r'orderproducts', OrderProducts, 'orderproduct')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
