from django.urls import path,include
from CryptoCrackers import views

app_name = 'CryptoCrackers'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('process_form/', views.process_form, name='process_form'),
    path('account/',include('allauth.urls'))
]
