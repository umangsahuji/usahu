from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('index',views.index,name='index'),
    path('shop',views.shop,name='shop'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('change_password',views.change_password,name='change_password'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('new_password',views.new_password,name='new_password'),
    path('contact',views.contact,name='contact'),
    path('blog',views.blog,name='blog'),
    path('seller_index',views.seller_index,name='seller_index'),
    path('seller_home',views.seller_home,name='seller_home'),
    path('seller_add_product',views.seller_add_product,name='seller_add_product'),
    path('seller_product_details/<int:pk>/',views.seller_product_details,name='seller_product_details'),
    path('seller_edit_product/<int:pk>/',views.seller_edit_product,name='seller_edit_product'),
    path('seller_delet_product/<int:pk>/',views.seller_delet_product,name='seller_delet_product'),
    path('product_details/<int:pk>/',views.product_details,name='product_details'),
    path('cart',views.cart,name='cart'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('remove_form_wishlist/<int:pk>/',views.remove_form_wishlist,name='remove_form_wishlist'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('remove_form_cart/<int:pk>/',views.remove_form_cart,name='remove_form_cart'),
    path('change_qty/<int:pk>/',views.change_qty,name='change_qty'),
    path('pay', views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),
    path('myorder/',views.myorder, name='myorder'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email')

    
]