from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.URLField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return f'{self.id} {self.title} {self.created_at}'
