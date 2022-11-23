from django.contrib import admin
from .models import Order, Ingredient


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'created_at',
        'paid',
        'value',
        'levels',
        'shape',
        'delivery_address',
        'delivery_time'
    )
    list_filter = ('status',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    list_filter = ('type',)
