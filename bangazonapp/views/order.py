from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Order, Customer, Payment


"""Author: Krystal Gates
Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries for orders.
Methods: GET DELETE(id) POST"""


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'payment', 'customer', 'created_date')

        depth = 1


class Orders(ViewSet):
    """Orders for BangazonApp"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """

        new_order = Order()
        foo = request.data.get("payment_id", None)
        if foo is not None:
            payment = Payment.objects.get(pk=request.data["payment_id"])
            new_order.payment = payment
            customer = Customer.objects.get(pk=request.data["customer_id"])
            new_order.customer = customer
        else:
            customer = Customer.objects.get(pk=request.data["customer_id"])
            new_order.customer = customer

        new_order.save()

        serializer = OrderSerializer(new_order, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for orders

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        payment = Payment.objects.get(pk=request.data["payment_id"])
        order.payment = payment
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of orders with customer
        """
        orders = Order.objects.all()

        customer = self.request.query_params.get('customer', None)
        payment = self.request.query_params.get('payment', None)
        if customer is not None:
            orders = orders.filter(customer__id=customer)
        if payment is not None:
            orders = orders.filter(payment__id=payment)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)