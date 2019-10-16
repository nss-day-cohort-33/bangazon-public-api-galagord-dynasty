from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Order, Customer, Payment, OrderProduct, Product
from .orderproduct import OrderProductSerializer
from .product import ProductSerializer

"""Author: Krystal Gates
Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries for orders.
Methods: GET DELETE(id) POST"""


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    line_items = ProductSerializer(many=True)
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'payment','customer_id', 'customer', 'created_date', 'line_items')
        depth = 1


class Orders(ViewSet):
    """Orders for BangazonApp"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Product instance
        """

        # Changing the orders resource by adding a product to an order means we have to make a new instance of OrderProduct. Let's do that first and add the product to it that was sent in the POST request:
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        # Now, we need to know whether order_item's order will be an existing order _or_ a new order we'll have to create:
        current_customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.filter(customer=current_customer, payment=None)

        # order is now either an existing, open order, or an empty queryset. How do we check? A new friend called exists()!
        if order.exists():
            print("Open order in db. Add it and the prod to OrderProduct")
            order_item.order = order[0]
        else:
            print("No open orders. Time to make a new order to add this product to")
            new_order = Order()
            new_order.customer = current_customer
            new_order.save()
            order_item.order = new_order

        # order_item has a product and an order. It's ready to save now
        order_item.save()

        # Convert the order to json and send it back to the client
        serializer = OrderSerializer(order_item, context={'request': request})

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
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)
        
        payment = self.request.query_params.get('payment', None)

        if payment is not None:
            orders = orders.filter(payment=None)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)