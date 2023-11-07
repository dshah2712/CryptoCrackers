from django.urls import path,include
from CryptoCrackers import views

app_name = 'CryptoCrackers'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('process_form/', views.process_form, name='process_form'),
    path('account/',include('allauth.urls')),
    path('purchase/', views.create_transaction, name='purchase'),
    path('payment/', views.purchase_crypto, name='payment'),
    path('coins/<str:coin_name>/', views.dynamic_Crypto, name='dynamic_crypto'),
]