from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Product, CategoryType, Customer

"""Author: Krystal Gates
Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries.
Methods: GET DELETE(id) POST"""


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'description', 'quantity', 'price', 'creation_date', 'location', 'image', 'category_type_id', 'customer_id')
        depth = 1


class Products(ViewSet):
    """Products for BangazonApp"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        new_product = Product()
        new_product.name = request.data["name"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.price = request.data["price"]
        new_product.creation_date = request.data["creation_date"]
        new_product.location = request.data["location"]
        new_product.image = request.data["image"]
        category_type = CategoryType.objects.get(pk=request.data["category_type_id"])
        new_product.category_type = category_type
        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_product.customer = customer
        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products with customer and category type
        """
        products = Product.objects.all()

        category_type = self.request.query_params.get('category_type', None)
        customer = self.request.query_params.get('customer', None)
        if category_type is not None:
            products = products.filter(category_type__id=category_type)
        if customer is not None:
            products = products.filter(customer__id=customer)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)