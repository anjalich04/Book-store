from django.db import models
import datetime
import os
from django.contrib.auth.models import User

def get_file_path(instance, filename):
    original_filename = filename
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "%s%s" % (now_time, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=False, blank=False)
    description = models.TextField(max_length=150, null=False, blank=False)
    status = models.BooleanField(default=False,help_text="0=default,1-Hidden")
    trending = models.CharField(max_length=20,null=False,blank=False)
    meta_title = models.CharField(max_length=50,null=False,blank=False)
    meta_keyword = models.CharField(max_length=50,null=False,blank=False)
    meta_description = models.TextField(max_length=100,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.CharField(max_length=50,null=False,blank=False)
    name = models.CharField(max_length=50,null=False,blank=False)
    product_image = models.ImageField(upload_to=get_file_path,null=False,blank=False)
    small_description = models.TextField(max_length=150,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    description = models.TextField(max_length=250,null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0=default,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0=default,1-Trending")
    tag=models.CharField(max_length=15,null=False,blank=False)
    meta_title = models.CharField(max_length=100,null=False,blank=False)
    meta_keyword = models.CharField(max_length=100,null=False,blank=False)
    meta_description = models.TextField(max_length=150,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=100,null=False,blank=False)
    lname = models.CharField(max_length=100,null=False,blank=False)
    email = models.CharField(max_length=100,null=False,blank=False)
    phone = models.CharField(max_length=50,null=False,blank=False)
    address = models.TextField(null=False,blank=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    country = models.CharField(max_length=50,null=False,blank=False)
    pincode = models.CharField(max_length=50,null=False,blank=False)
    total_price = models.FloatField(null=False,blank=False)
    payment_mode = models.CharField(max_length=50,null=False,blank=False)
    payment_id = models.CharField(max_length=50,null=False,blank=False)

    orderstatus = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Completed", "Completed"),
    )
    status = models.CharField(max_length=50,choices=orderstatus,default="Pending")
    message=models.TextField(null=False,blank=False)
    tracking_no = models.CharField(max_length=50,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} = {}'.format(self.id,self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return '{} = {}'.format(self.order.order.tracking_no)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,null=False,blank=False)
    address = models.TextField(null=False,blank=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    country = models.CharField(max_length=50,null=False,blank=False)
    pincode = models.CharField(max_length=50,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name




