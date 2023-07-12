from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
