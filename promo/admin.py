from django.contrib import admin

from promo.models import Promo


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    model = Promo
    fields = ('user', 'text')
