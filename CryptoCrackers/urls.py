from django.urls import path, include, path
from CryptoCrackers import views

app_name = 'CryptoCrackers'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('process_form/', views.process_form, name='process_form'),
    path('account/',include('allauth.urls')),
    path('coins/<str:coin_name>/', views.dynamic_Crypto, name='dynamic_crypto'),
    path('userprofile/', views.user_profile, name='profile'),
    path('userprofile/accountsecurity/', views.passwd_change, name='change password'),
    path('userprofile/delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.user_logout, name='logout'),
    path('add_to_wishlist/<str:coin_name>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('userprofile/remove_to_wishlist/<str:coin_name>/', views.remove_to_wishlist, name='remove-to-wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('landing/', views.landing, name='landing'),
    path('add_money/', views.add_money, name='add_money'),
    path('purchase_currency/', views.purchase_currency, name='purchase_currency'),
    # path('home/', views.homePage, name='home'),
    ]