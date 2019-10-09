from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import OrderProduct, Order, Product


"""Author: Krystal Gates
Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries for orderproduct.
Methods: GET DELETE(id) POST"""


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers
    """

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product', 'quantity')

        depth = 2


class OrderProducts(ViewSet):
    """Orders for BangazonApp"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized OrderProduct instance
        """
        new_orderproduct = OrderProduct()
        order = Order.objects.get(pk=request.data["order_id"])
        new_orderproduct.order = order
        product = Product.objects.get(pk=request.data["product_id"])
        new_orderproduct.product = product
        new_orderproduct.quantity = request.data["quantity"]

        new_orderproduct.save()

        serializer = OrderProductSerializer(new_orderproduct, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single orderproduct

        Returns:
            Response -- JSON serialized orderproduct instance
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            orderproduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to orderproducts resource

        Returns:
            Response -- JSON serialized list of orderproducts
        """
        orderproducts = OrderProduct.objects.all()

        order = self.request.query_params.get('order', None)
        product = self.request.query_params.get('product', None)
        payment = self.request.query_params.get('payment', None)

        if product is not None:
            orderproducts = orderproducts.filter(product__id=product)
        if order is not None:
            orderproducts = orderproducts.filter(order_payment=None)
        # if payment is not None:
        #     orderproducts = orderproducts.filter(payment__none=None)


        serializer = OrderProductSerializer(
            orderproducts, many=True, context={'request': request})
        return Response(serializer.data)