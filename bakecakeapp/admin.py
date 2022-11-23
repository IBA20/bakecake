from django.contrib import admin
from .models import Order, Ingredient


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
