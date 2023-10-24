from django.urls import path
from CryptoCrackers import views

app_name = 'CryptoCrackers'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
