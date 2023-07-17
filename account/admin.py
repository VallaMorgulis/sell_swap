from django.contrib import admin

from account.models import CustomUser


@admin.register(CustomUser)
class AdminAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = ('id', 'user')
