from random import randint

from django.contrib.auth import get_user_model
from django.db import models
from category.models import Category
from ckeditor.fields import RichTextField

User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT,
                              related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def generate_name(self):
        return 'image' + str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(ProductImage, self).save(*args, **kwargs)


class Likes(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE, related_name='likes')

    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} -> {self.user} -> {self.is_liked}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} -> {self.user} -> {self.favorite}'
