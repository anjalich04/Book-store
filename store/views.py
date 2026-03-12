from django.shortcuts import render,redirect
from django.db.models import F
from . models import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def home(request):
    trending_products = Product.objects.filter(trending=1)
    featured_products = Product.objects.filter(status=0).order_by('-created_at')[:8]
    new_arrivals = Product.objects.filter(status=0).order_by('-created_at')[:8]
    best_sellers = Product.objects.filter(status=0, trending=1)[:8]
    recommended_products = Product.objects.filter(status=0).order_by('-created_at')[:8]
    discounted_products = Product.objects.filter(status=0, original_price__gt=F('selling_price'))[:8]
    categories = Category.objects.filter(status=0)[:8]
    context={
        "trending_products": trending_products,
        "featured_products": featured_products,
        "new_arrivals": new_arrivals,
        "best_sellers": best_sellers,
        "recommended_products": recommended_products,
        "discounted_products": discounted_products,
        "categories": categories,
    }
    return render(request,"store/home.html",context)

def collections(request):
    category = Category.objects.filter(status=0)
    context = {"category":category}
    return render(request,"store/collections.html",context)

def collectionsview(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products =Product.objects.filter(category__slug=slug)
        category=Category.objects.filter(slug=slug).first()
        context={'products':products,'category':category}
        return render(request,'store/products/home.html',context)
    else:
        messages.warning(request,"No such category found!")
        return redirect('collections')

def account(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    wishlist_count = wishlist_items.count()
    cart_count = Cart.objects.filter(user=request.user).count()
    recommendations = Product.objects.filter(status=0).order_by('-created_at')[:6]

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", request.user.first_name)
        request.user.last_name = request.POST.get("last_name", request.user.last_name)
        request.user.email = request.POST.get("email", request.user.email)
        request.user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("account")

    context = {
        "orders": orders,
        "wishlist_items": wishlist_items,
        "wishlist_count": wishlist_count,
        "cart_count": cart_count,
        "recommendations": recommendations,
    }
    return render(request, "store/account.html", context)

def authors(request):
    query = request.GET.get("q", "").strip()
    authors_qs = Product.objects.filter(status=0).values_list("author", flat=True).distinct().order_by("author")
    if query:
        authors_qs = authors_qs.filter(author__icontains=query)
    context = {"authors": authors_qs, "query": query}
    return render(request, "store/authors.html", context)

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")
            return redirect("account")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "store/change_password.html", {"form": form})

def productview(request,cate_slug,prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0).exists():
        if Product.objects.filter(category__slug=cate_slug, slug=prod_slug, status=0).exists():
            products = Product.objects.filter(category__slug=cate_slug, slug=prod_slug, status=0).first()
            related_products = list(Product.objects.filter(category=products.category, status=0).exclude(id=products.id)[:9])
            related_groups = [related_products[i:i+3] for i in range(0, len(related_products), 3)]
            context = {'products': products, 'related_products': related_products, 'related_groups': related_groups}
        else:
            messages.error(request,"no such product found!")
            return redirect("collections")
    else:
        messages.error(request,"no such category found")
        return redirect("collections")
    return render(request,"store/products/view.html",context)
