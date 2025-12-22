import random
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect,render
from django.contrib import messages
from django.http.response import JsonResponse
from store.models import Product, Cart, Profile, Order, OrderItem
from django.contrib.auth.models import User

def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_quantity > item.product.quantity:
            Cart.objects.delete(id=item.id)
    cartitem = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitem:
        total_price = total_price+item.product.selling_price * item.product_quantity

    context = {'cartitem':cartitem, 'total_price':total_price}
    return render(request, 'store/checkout.html', context)

def placeorder(request):
    if request.method == "POST":
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user).exists():
            userprofile = Profile(
                user=request.user,
                phone=request.POST.get('phone'),
                address=request.POST.get('Address'),
                city=request.POST.get('City'),
                state=request.POST.get('State'),
                country=request.POST.get('Country'),
                pincode=request.POST.get('Pincode'),
            )
            userprofile.save()

        neworder = Order(
            user=request.user,
            fname=request.POST.get('firstname'),
            lname=request.POST.get('lastname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('Address'),
            city=request.POST.get('City'),
            state=request.POST.get('State'),
            country=request.POST.get('Country'),
            pincode=request.POST.get('Pincode'),
            payment_mode=request.POST.get('payment_mode'),
        )

        if neworder.payment_mode == "Paid by Razorpay":
            neworder.payment_id = request.POST.get('payment_id')
        else:
            neworder.payment_id = "COD"

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(
            item.product.selling_price * item.product_quantity for item in cart
        )
        neworder.total_price = cart_total_price

        trackno = "Anjali" + str(random.randint(111111, 999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = "Anjali" + str(random.randint(111111, 999999))

        neworder.tracking_no = trackno
        neworder.save()

        # ✅ CREATE ORDER ITEMS
        for item in cart:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_quantity
            )

            # ✅ REDUCE STOCK
            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.product_quantity
            product.save()

        # ✅ CLEAR CART
        Cart.objects.filter(user=request.user).delete()

        messages.success(request, 'Your order has been placed successfully')

        if neworder.payment_mode == "Paid by Razorpay":
            return JsonResponse({'status': 'Your order has been placed successfully'})

        return redirect('order')   # ✅ FIXED

    return redirect('checkout')

def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price * item.product_quantity
    return JsonResponse({'total_price': total_price})







