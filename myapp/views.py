from django.shortcuts import render,redirect
from .models import User,Contact,Product,Wishlist,Cart,Transaction
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
# Create your views here.
def contact(request):
	if request.method=='POST':
		Contact.objects.create(
			fname=request.POST['fname'],
			email=request.POST['email'],
			contact=request.POST['contact'],
			desc=request.POST['desc']
			)
		msg='contact save successfuly'
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def index(request):
	return render(request,'index.html')
def blog(request):
	return render(request,'blog.html')

def home(request):
	products=Product.objects.all()
	return render(request,'home.html',{'products':products})

def shop(request):		
	products=Product.objects.all()
	return render(request,'shop.html',{'products':products})

def signup(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			msg='email is already registered'
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],		
					profile_pic=request.FILES['profile_pic'],
					address=request.POST['address'],
					password=request.POST['password'],
					usertype=request.POST['usertype'],
					)
				msg='signup successfuly'
				return render(request,'signup.html',{'msg':msg})
			else:
				msg='password and confirm password'
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password'],
				)
			if user.usertype=='user':
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				wishlist=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlist)
				carts=Cart.objects.filter(user=user,status="pending")
				for i in carts:
					net_price=0
					net_price=net_price+i.total_price
				request.session['cart_count']=len(carts)
				return redirect('home')
				
			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				return redirect('seller_home')
		except:
			msg='email id  and password does not match'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')
def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.address=request.POST['address']
		user.mobile=request.POST['mobile']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg='user update successfuly'

		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'profile.html',{'user':user})



def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password== request.POST['oldpassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg='new password and confirm password does not match'
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg='old password does  not match'
			return render(request,'change_password.html',{'msg':msg})
	else:
		return render(request,'change_password.html')
def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			print(user)
			subject = 'OTP For Forgot Password'
			otp=random.randint(1000,9999)
			message = 'Your OTP For Forgot Password Is '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp,'email':user.email})
		except Exception as e:
			print(e)
			msg="Email Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
		return render(request,'forgot_password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']
	if uotp==otp:
		return render(request,'new_password.html',{'email':email})
	else:
		msg='otp does not match'
		return render(request,'verify_otp',{'email':email,'otp':otp})

def new_password(request):
	npassword=request.POST['npassword']
	cpassword=request.POST['cpassword']
	email=request.POST['email']
	if npassword==cpassword:
		user=User.objects.get(email=request.POST['email'])
		user.password=npassword
		user.save()
		return redirect(login)
	else:
		msg='password and confirm does not match'
		return render(request,'new_password.html',{'msg':msg,'email':email})

def seller_home(request):
	products=Product.objects.all()
	return render(request,'seller_home.html',{'products':products})

def seller_index(request):
	return render(request,'seller_index.html')

def seller_add_product(request):
	if request.method=='POST':
		seller=User.objects.get(email=request.session['email'])
		Product.objects.create(
			seller=seller,
			product_weight=request.POST['product_weight'],
			product_material=request.POST['product_material'],
			product_color=request.POST['product_color'],
			product_desc=request.POST['product_desc'],
			product_price=request.POST['product_price'],
			product_img=request.FILES['product_img'],
			product_size=request.POST['product_size'],
			product_img1=request.FILES['product_img1'],
			product_img2=request.FILES['product_img2'],
			product_img3=request.FILES['product_img3'],
			product_name=request.POST['product_name'],

			)
		msg='Producr add successfuly'
		return render(request,'seller_add_product.html',{'msg':msg})
	else:
		return render(request,'seller_add_product.html')

def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller_product_details.html',{'product':product})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=='POST':
		product.product_weight=request.POST['product_weight']
		product.product_material=request.POST['product_material']
		product.product_color=request.POST['product_color']
		product.product_price=request.POST['product_price']
		product.product_size=request.POST['product_size']
		product.product_desc=request.POST['product_desc']
		product.product_name=request.POST['product_name']
		try:
			product.product_img1=request.FILES['product_img1']
		except:
			pass	
		try:
			product.product_img2=request.FILES['product_img2']
		except:
			pass
		try:	
			product.product_img3=request.FILES['product_img3']
		except:
			pass
		try:
			product.product_img=request.FILES['product_img']
		except:
			pass
		product.save()
		msg='product details update successfuly '
		return render(request,'seller_edit_product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller_edit_product.html',{'product':product})


def seller_delet_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller_home')

def product_details(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist_flag=False
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	cart_flag=False
	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass
	return render(request,'product_details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	return render(request,'cart.html',{'product':product,'user':user})


def add_to_wishlist(request,pk):
	if "email" in request.session:
		product=Product.objects.get(pk=pk)
		user=User.objects.get(email=request.session['email'])
		Wishlist.objects.create(
			product=product,
			user=user,
			)
		wishlist=Wishlist.objects.filter(user=user)
		request.session['wishlist_count']=len(wishlist)
		return render(request,'wishlist.html')
	else:
		return redirect("wishlist")
			
	
def wishlist(request):
	if "email" in request.session:
		user=User.objects.get(email=request.session['email'])
		wishlists=Wishlist.objects.filter(user=user)
		return render(request,'wishlist.html',{'wishlists':wishlists})
	else:
		return redirect('home')
			

def remove_form_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	wishlist=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlist)
	return render(request,'home.html')

def add_to_cart(request,pk):
	if "email" in request.session:
		product=Product.objects.get(pk=pk)
		user=User.objects.get(email=request.session['email'])
		Cart.objects.create(
			product=product,
			user=user,
			product_price=product.product_price,
			total_price=product.product_price
			)
		return redirect('cart')
	else:
		return redirect("cart")

def cart(request):
	if "email" in request.session:
		net_price=0
		user=User.objects.get(email=request.session['email'])
		carts=Cart.objects.filter(user=user,status="pending")
		for i in carts:
			net_price=net_price+i.total_price
		request.session['net_price']=net_price
		request.session['cart_count']=len(carts)
		return render(request,'cart.html',{'carts':carts,'net_price':net_price})
	else:
		return redirect('cart')

def remove_form_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	carts=Cart.objects.get(user=user,product=product)
	carts.delete()
	return render(request,'home.html')

def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return render(request,'cart.html')

def initiate_payment(request):
	user=User.objects.get(email=request.session['email'])
	try:
		amount = int(request.POST['amount'])
	except:
		return render(request, 'cart.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = Transaction.objects.create(made_by=user, amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY

	params = (
		('MID', settings.PAYTM_MERCHANT_ID),
		('ORDER_ID', str(transaction.order_id)),
		('CUST_ID', str('usahu3589@gmail.com')),
		('TXN_AMOUNT', str(transaction.amount)),
		('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
		('WEBSITE', settings.PAYTM_WEBSITE),
		# ('EMAIL', request.user.email),
		# ('MOBILE_N0', '9911223388'),
		('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
		('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
		# ('PAYMENT_MODE_ONLY', 'NO'),
	)

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()
	carts=Cart.objects.filter(user=user)
	for i in carts:
		i.status='paid'
		i.save()

	paytm_params['CHECKSUMHASH'] = checksum
	print('SENT: ', checksum)
	return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
		# Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
		if is_valid_checksum:
			received_data['message'] = "Checksum Matched"
		else:
			received_data['message'] = "Checksum Mismatched"
			return render(request, 'callback.html', context=received_data)
		return render(request, 'callback.html', context=received_data)

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,status='paid')
	return render(request,'myorder.html',{'carts':carts})

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)
