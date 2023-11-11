from django.contrib import admin
from .models import UserDetails,CryptoCurrency,Transactions, News

admin.site.register(UserDetails)
admin.site.register(CryptoCurrency)
admin.site.register(Transactions)
admin.site.register(News)

# Register your models here.
