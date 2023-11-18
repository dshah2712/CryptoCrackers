from django.contrib import admin
from .models import UserDetails, CryptoCurrency, News, Wallet, Purchase, Transaction

admin.site.register(UserDetails)
admin.site.register(CryptoCurrency)
admin.site.register(Wallet)
admin.site.register(Purchase)
admin.site.register(Transaction)
admin.site.register(News)

# Register your models here.
