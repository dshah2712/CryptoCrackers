from django.urls import path, include, path
from CryptoCrackers import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'CryptoCrackers'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('send_forgotpassword/', views.send_forgotpassword_mail, name='send_forgotpassword_mail'),
    path('forgotpassword',views.forgot_password,name="forgotpassword"),
    path('changepassword',views.change_password,name="changepassword"),
    path('process_form/', views.process_form, name='process_form'),
    path('account/',include('allauth.urls')),
    path('coins/<str:coin_name>/', views.dynamic_Crypto, name='dynamic_crypto'),
    path('userprofile/', views.user_profile, name='profile'),
    path('userprofile/accountsecurity/', views.acc_sec, name='acc_sec'),
    path('userprofile/delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.user_logout, name='logout'),
    # path('home/', views.homePage, name='home'),
    path('add_to_wishlist/<str:coin_name>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove_to_wishlist/<str:coin_name>/', views.remove_to_wishlist, name='remove-to-wishlist'),
    path('remove_to_wishlist/<str:coin_name>/', views.remove_to_wishlist, name='remove-to-wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('', views.landing, name='landing'),
    path('userprofile/add_money', views.add_money, name='add_money'),
    path('userprofile/purchase_currency/', views.purchase_currency, name='purchase_currency'),
    path('sell_crypto/', views.Sell, name='sell_crypto'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('purchasehistory_list/', views.purchase_history_list, name='purchasehistory_list'),
    path('portfolio/', views.portfolio, name='portfolio'),

    # path('add_money/', views.add_money, name='add_money'),
    # path('purchase_currency/', views.purchase_currency, name='purchase_currency'),
    ]
