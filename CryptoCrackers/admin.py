from django.contrib import admin
from .models import UserDetails,CryptoCurrency,Transactions

admin.site.register(UserDetails)
admin.site.register(CryptoCurrency)
admin.site.register(Transactions)

# Register your models here.
