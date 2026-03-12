from .models import Category, Product, Cart, Wishlist


def navbar_categories(request):
    categories = Category.objects.filter(status=0).order_by("name")
    product_names = list(Product.objects.filter(status=0).values_list("name", flat=True)[:30])
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return {
        "nav_categories": categories,
        "nav_products": product_names,
        "nav_cart_count": cart_count,
        "nav_wishlist_count": wishlist_count,
    }
