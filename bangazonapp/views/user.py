from django.contrib.auth.models import User
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()