from django.db import models


class PageView(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.page} - {self.timestamp}'
