from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Promo(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             related_name='promo')
    image = models.ImageField(upload_to='images')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'promo'
        verbose_name_plural = 'promo'

    def __str__(self):
        return f'{self.user} - {self.text[:25]}'
