from django.urls import path,include
from CryptoCrackers import views

app_name = 'CryptoCrackers'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('process_form/', views.process_form, name='process_form'),
    path('account/',include('allauth.urls'))
]
