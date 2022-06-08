from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to='user_profile')
	usertype=models.CharField(max_length=100,default='User')
	def __str__(self):
		return  self.fname+ '=' + self.lname

class Contact(models.Model):
	fname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	contact=models.CharField(max_length=100)
	desc=models.TextField()
	def __str__(self):
		return self.fname
 
class Product(models.Model):
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_weight=models.CharField(max_length=100,default='')
	product_material=models.CharField(max_length=100,default='')
	product_desc=models.TextField()
	product_color=models.CharField(max_length=100,default='')
	product_size=models.CharField(max_length=100,default='')
	product_img=models.ImageField(upload_to='product_images')
	product_img1=models.ImageField(upload_to='product_images',default='')
	product_img2=models.ImageField(upload_to='product_images',default='')
	product_img3=models.ImageField(upload_to='product_images',default='')
	product_name=models.CharField(max_length=100,default='')
	product_price=models.CharField(max_length=100,default='')
	def __str__ (self):
		return self.seller.fname+ '='+ self.product_name

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+ '=' +self.product.product_name

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_price=models.IntegerField()
	product_qty=models.IntegerField(default=1)
	total_price=models.IntegerField()
	status=models.CharField(max_length=100,default='pending')
	
	def __str__(self):
		return self.user.fname+ '=' +self.product.product_name

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
