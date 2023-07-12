from django.contrib import admin

from product.models import Product, ProductImage


class ImageInLineAdmin(admin.TabularInline):
    model = ProductImage
    fields = ('image', )
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin, ]
