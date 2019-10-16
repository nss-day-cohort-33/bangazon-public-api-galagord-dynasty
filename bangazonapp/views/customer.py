"""View module for handling requests about Customers"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Customer
from rest_framework.decorators import action


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'address', 'phone_number')
        depth = 1


class Customers(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Author: Shane Miller
        Purpose: Allow a user to communicate with the Bangazon database to retrieve  customer
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    """Customers for Bangazon"""

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        customers = Customer.objects.all()
        customer = Customer.objects.get(user=request.auth.user)
        customers = Customer.objects.filter(customer=customer)


        serializer = CustomerSerializer(
            customers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


    @action(methods=['get'], detail=False)
    def one_customer(self, request):

        current_user = Customer.objects.get(user=request.auth.user)

        serializer = CustomerSerializer(current_user, many=False, context={'request': request})
        return Response(serializer.data)