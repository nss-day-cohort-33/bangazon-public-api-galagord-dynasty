from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Payment, Customer
from .customer import CustomerSerializer

"""Author: Adam Knowles
    Purpose: Allow a user to communicate with the Bangazon database to GET and POST entries.
    Methods: GET POST"""


class PaymentSerializer(serializers.HyperlinkedModelSerializer):



    """JSON serializer for Payments

    Arguments:
        serializers
    """
    class Meta:
        model = Payment
        url = serializers.HyperlinkedIdentityField(
            view_name='payment',
            lookup_field='id'

        )
        fields = ('id', 'url', 'merchant_name', 'account_number', 'created_date', 'expiration_date', 'customer')
        depth = 2


class Payments(ViewSet):
    """Payments for Bangazon LLC"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment instance
        """
        new_payment = Payment()
        new_payment.merchant_name = request.data["merchant_name"]
        new_payment.account_number = request.data["account_number"]
        new_payment.expiration_date = request.data["expiration_date"]


        customer = Customer.objects.get(user=request.auth.user)
        new_payment.customer = customer
        new_payment.save()

        serializer = PaymentSerializer(new_payment, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single payment

        Returns:
            Response -- JSON serialized payment instance
        """
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to payment resource

        Returns:
            Response -- JSON serialized list of payments
        """
        payments = Payment.objects.all()

        # Support filtering payments by customer id
        customer = Customer.objects.get(user=request.auth.user)
        payments = Payment.objects.filter(customer=customer)

        serializer = PaymentSerializer(
            payments, many=True, context={'request': request})
        return Response(serializer.data)