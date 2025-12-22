from django.shortcuts import redirect,render
from django.contrib import messages
from django.http.response import JsonResponse
from store.models import Product,Cart


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.filter(id=prod_id).first()
            if(product_check):
                if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                    return JsonResponse({"status":'product already in cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product=product_check, product_quantity=prod_qty)
                        return JsonResponse({"status":'product added to cart'})
                    else:
                        return JsonResponse({"status": "Only {} quantity available".format(product_check.quantity)})
            else:
                return JsonResponse({"status": "No such product"})
        else:
            return JsonResponse({"status":'Login to continue'})
    return JsonResponse({"status": "Invalid Access"})

def viewcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        context = {'cart': cart}
        return render(request, "store/cart.html", context)
    else:
        return redirect('loginpage')

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id,user=request.user)
            cart.product_quantity = prod_qty
            cart.save()
            return JsonResponse({"status":'updated successfully'})
    return JsonResponse({"status": "Invalid Access"})
#
# def deletecart(request):
#     if request.method == 'POST':
#         prod_id = int(request.POST.get('product_id'))
#         if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
#             cartitem = Cart.objects.get(user=request.user, product_id=prod_id)
#             cartitem.delete()
#             return JsonResponse({"status":'deleted successfully'})
#     return JsonResponse({"status": "Invalid Access"})

def deletecartitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                cartitem = Cart.objects.get(user=request.user, product_id=prod_id)
                cartitem.delete()
                return JsonResponse({'status': "Item removed from cart"})
            else:
                return JsonResponse({'status': "Item not found in cart"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return JsonResponse({'status': "Invalid request"})