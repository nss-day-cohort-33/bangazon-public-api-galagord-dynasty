"""Author: Misty M. DeRamus
Purpose:
Methods: GET
View module for handling requests about types of categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import CategoryType, Product
from .product import ProductSerializer


class CategoryTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for types of categories

    Arguments:
        serializers
    """
    products = ProductSerializer(many=True)
    class Meta:
        model = CategoryType
        url = serializers.HyperlinkedIdentityField(
            view_name='categorytype',
            lookup_field='pk'
        )
        fields = ('id', 'url', 'name', 'products')
        depth = 2

class PureCategoryTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for types of categories

    Arguments:
        serializers
    """
    class Meta:
        model = CategoryType
        url = serializers.HyperlinkedIdentityField(
            view_name='categorytype',
            lookup_field='pk'
        )
        fields = ('id', 'url', 'name')
        depth = 2

class CategoryTypes(ViewSet):
    """Product category types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized CategoryType model instance
        """
        new_category = CategoryType()
        new_category.name = request.data["name"]
        new_category.save()

        serializer = CategoryTypeSerializer(new_category, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized Category instance
        """
        try:
            category = CategoryType.objects.get(pk=pk)
            serializer = CategoryTypeSerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
            """Handle GET requests to Category resource

            Returns:
                Response -- JSON serialized list of category types
            """
            categories = CategoryType.objects.all()

            limit = self.request.query_params.get('limit', None)
            if limit is not None:
                for category in categories:
                    related_products = Product.objects.filter(category_type=category)
                    category.products = list(related_products)[:3]
                serializer = CategoryTypeSerializer(
                categories, many=True, context={'request': request})
            else: 
                serializer = PureCategoryTypeSerializer(
                categories, many=True, context={'request': request})

            return Response(serializer.data)
