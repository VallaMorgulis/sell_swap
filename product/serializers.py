from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Product, ProductImage, Likes, Favorite
from category.models import Category


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email', 'category_name', 'title',
                  'price', 'preview')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, read_only=True)
    # owner_email = serializers.ReadOnlyField(source='owner.email')
    # owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'

            #(
            #'id', 'owner', 'owner_email', 'title', 'description', 'category',
            #'price', 'quantity', 'created_at', 'updated_at', 'preview', 'images'
       # )

    @staticmethod
    def get_stars(instance):
        stars = {
            '5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
            '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
            '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['ratings_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        product = Product.objects.create(**validated_data)

        count = 0
        for image in images:
            if count >= 5:
                break
            ProductImage.objects.create(image=image, product=product)
            count += 1

        return product
