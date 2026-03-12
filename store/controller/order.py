from django.shortcuts import redirect, render
from django.contrib import messages
from store.models import Order, OrderItem

def order_view(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,"store/order.html",context)

def view_order(request,t_no):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    if not order:
        messages.error(request, "Order not found.")
        return redirect('order')
    orderitems = OrderItem.objects.filter(order=order)
    context = {"order":order,"orderitems":orderitems}
    return render(request,"store/orderitem.html",context)
