from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Product, CategoryType, Customer
from rest_framework.decorators import action


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
        fields = ('id', 'url', 'name', 'description', 'quantity', 'price', 'creation_date', 'location', 'image', 'category_type', 'customer')

        depth = 2


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
        new_product.location = request.data["location"]
        # new_product.image = request.data["image"]
        category_type = CategoryType.objects.get(pk=request.data["category_type_id"])
        new_product.category_type = category_type
        customer = Customer.objects.get(user=request.auth.user)
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
            # customer = Product.objects.get(pk=pk)
            # found this line in another repo and wondered if it can be utilized by us ?
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
        product_list = []

        # filter by category_type id
        category_type = self.request.query_params.get('category_type', None)
        if category_type is not None:
            products = products.filter(category_type__id=category_type)
        
        #filter by location id
        location = self.request.query_params.get('location', None)
        category_type = self.request.query_params.get('category', None)
        quantity = self.request.query_params.get('quantity', None)

        if location == "":
            products = Product.objects.all()
        elif location is not None:
            products = Product.objects.filter(location=location.lower())

        # if category_type is not None:
        #     products = products.filter(producttype__id=category_type)
        #     for product in products:
        #         if product.quantity > 0:
        #             product_list.append(product)
        #     products = product_list

        # if quantity is not None:
        #     quantity = int(quantity)
        #     length = len(products)
        #     new_products = list()
        #     count = 0
        #     for product in products:
        #         count += 1
        #         if count - 1 + quantity >= length:
        #             new_products.append(product)
        #             if count == length:
        #                 products = new_products
        #                 break

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def myproducts(self, request):
        current_user = Customer.objects.get(user=request.auth.user)
        products = Product.objects.all()
        products = products.filter(customer=current_user)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
