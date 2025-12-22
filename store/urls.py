from django.urls import path
from . import views
from store.controller import authview,cart,wishlist,checkout,order

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:cate_slug>/<str:prod_slug>/', views.productview, name='productview'),
    path('collections/<str:slug>/', views.collectionsview, name='collectionsview'),

    path('register/',authview.register, name='register'),
    path('login/',authview.loginpage, name='loginpage'),
    path('logout/',authview.logoutpage, name='logoutpage'),

    path('addtocart/', cart.addtocart, name='addtocart'),
    path('cart/', cart.viewcart, name='cart'),
    path('update-cart/', cart.updatecart, name='update-cart'),
    path('delete-cart-item/', cart.deletecartitem, name='delete-cart-item'),

    path('wishlist/',wishlist.index, name='wishlist'),
    path('add-to-wishlist/',wishlist.addtowishlist, name='add-to-wishlist'),
    path('delete-wishlist-item/',wishlist.deletewishlistitem, name='delete-wishlist-item'),

    path('checkout/',checkout.index, name='checkout'),
    path('place-order/',checkout.placeorder, name='place-order'),
    path('proceed-to-pay/',checkout.razorpaycheck,name='proceed-to-pay'),

    path('order/',order.order_view,name='order'),
    path('view-order/<str:t_no>/',order.view_order,name='orderview'),

]
