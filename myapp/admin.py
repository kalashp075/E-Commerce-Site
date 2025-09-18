from django.contrib import admin
from .models import Product, Cart, CartItem, ProductDetail, Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'birthdate')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'brand', 'description')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'strap_material']
    search_fields = ['product__name', 'strap_material']

admin.site.register(ProductDetail, ProductDetailAdmin)