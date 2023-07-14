from django.db.models import Avg, Count
from rest_framework import serializers
from .models import Product, ProductImage, Likes, Favorite


class RecommendedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'preview')


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    category_name = serializers.ReadOnlyField(source='category.name')
    recommended_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email', 'category_name', 'title',
                  'price', 'preview', 'recommended_products')

    def get_recommended_products(self, instance):
        recommended_products = Product.objects.order_by('-rating').exclude(id=instance.id)[:5]
        serializer = RecommendedProductSerializer(recommended_products, many=True)
        return serializer.data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    recommended_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'owner_email', 'title', 'description', 'category',
            'price', 'quantity', 'created_at', 'updated_at', 'preview', 'images', 'recommended_products'
        )

    def get_recommended_products(self, instance):
        recommended_products = Product.objects.order_by('-rating').exclude(id=instance.id)[:5]
        serializer = RecommendedProductSerializer(recommended_products, many=True)
        return serializer.data

    @staticmethod
    def get_stars(instance):
        stars = {
            '5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
            '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
            '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        request = self.context.get('request')
        repr = super().to_representation(instance)
        rating = instance.reviews.aggregate(Avg('rating'), Count('rating'))
        repr['rating'] = {
            'average': rating['rating__avg'] or 0.0,
            'ratings_count': rating['rating__count']
        }
        repr['stars'] = self.get_stars(instance)
        repr['likes_count'] = instance.likes.filter(is_liked=True).count()
        repr['liked_by_user'] = False
        repr['favorite_by_user'] = False
        if request:
            if request.user.is_authenticated:
                repr['liked_by_user'] = Likes.objects.filter(user=request.user, product=instance,
                                                             is_liked=True).exists()
                repr['favorite_by_user'] = Favorite.objects.filter(user=request.user, favorite=True,
                                                                   product=instance).exists()
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


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["author"] = instance.author.email
        repr["category"] = instance.category.title
        return repr
