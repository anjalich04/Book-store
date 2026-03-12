from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from store.models import Product, Wishlist

def index(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, "store/wishlist.html", context)

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                prod_id = int(request.POST.get('product_id'))
            except (TypeError, ValueError):
                return JsonResponse({"status": "Invalid product"})

            product_check = Product.objects.filter(id=prod_id, status=0).first()
            if not product_check:
                return JsonResponse({'status': 'No such product found'})

            if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                return JsonResponse({"status": "Product already in wishlist"})

            Wishlist.objects.create(user=request.user, product_id=prod_id)
            return JsonResponse({'status': 'Product added to wishlist'})
        else:
            return JsonResponse({'status':'Login to continue'})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                prod_id = int(request.POST.get('product_id'))
            except (TypeError, ValueError):
                return JsonResponse({"status": "Invalid product"})

            wishlist_item = Wishlist.objects.filter(user=request.user, product_id=prod_id).first()
            if wishlist_item:
                wishlist_item.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status':'Login to continue'})
    return redirect('/')
