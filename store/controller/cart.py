from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from store.models import Product, Cart

def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                prod_id = int(request.POST.get('product_id'))
            except (TypeError, ValueError):
                return JsonResponse({"status": "Invalid product"})

            product_check = Product.objects.filter(id=prod_id, status=0).first()
            if not product_check:
                return JsonResponse({'status': 'No such product found'})

            if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                return JsonResponse({"status": 'Product already in cart'})

            try:
                prod_qty = int(request.POST.get('product_qty'))
            except (TypeError, ValueError):
                prod_qty = 1

            if prod_qty < 1:
                prod_qty = 1

            if product_check.quantity >= prod_qty:
                Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                return JsonResponse({'status': 'Product added successfully'})
            return JsonResponse({'status': 'Only ' + str(product_check.quantity) + " available"})
        else:
            return JsonResponse({'status':'Login to continue'})
    return redirect('/')

def viewcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_price = 0
        for item in cart:
            total_price += item.product.selling_price * item.product_qty
        context = {'cart': cart, 'total_price': total_price}
        return render(request,'store/cart.html',context)
    else:
        return redirect('loginpage')

def updatecart(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "Login to continue"})

        try:
            prod_id = int(request.POST.get('product_id'))
        except (TypeError, ValueError):
            return JsonResponse({"status": "Invalid product"})

        cart_item = Cart.objects.filter(user=request.user, product_id=prod_id).first()
        if cart_item:
            try:
                prod_qty = int(request.POST.get('product_qty'))
            except (TypeError, ValueError):
                prod_qty = cart_item.product_qty

            if prod_qty < 1:
                prod_qty = 1

            if cart_item.product.quantity >= prod_qty:
                cart_item.product_qty = prod_qty
                cart_item.save()
                return JsonResponse({"status": "Updated Successfully"})
            return JsonResponse({"status": "Only " + str(cart_item.product.quantity) + " available"})
    return redirect('/')

def deletecartitem(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "Login to continue"})

        try:
            prod_id = int(request.POST.get('product_id'))
        except (TypeError, ValueError):
            return JsonResponse({"status": "Invalid product"})

        cartitem = Cart.objects.filter(product_id=prod_id, user=request.user).first()
        if cartitem:
            cartitem.delete()
            return JsonResponse({'status': 'Delete successfully'})
    return redirect('/')



