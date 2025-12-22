from django.contrib import admin
from django.contrib.auth.models import User

from .models import Category, Product, Cart, Wishlist, Order, OrderItem, Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
