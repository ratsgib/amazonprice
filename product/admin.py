from django.contrib import admin
from .models import Product, Price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "asin", "created_date"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["product", "price", "created_date"]
