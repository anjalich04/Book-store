from django.contrib import admin
from .models import Category, Product, Cart, Wishlist, Order, OrderItem, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "status", "trending", "created_at")
    list_filter = ("status", "trending", "created_at")
    search_fields = ("name", "slug", "meta_title", "meta_keyword")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "category", "selling_price", "quantity", "status", "trending")
    list_filter = ("status", "trending", "category")
    search_fields = ("name", "author", "slug", "tag", "meta_title", "meta_keyword")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "product_qty", "created_at")
    search_fields = ("user__username", "product__name")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_at")
    search_fields = ("user__username", "product__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "tracking_no", "user", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("tracking_no", "user__username", "email", "phone")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "price", "quantity")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "city", "state", "country")
    search_fields = ("user__username", "phone", "city", "state", "country")
