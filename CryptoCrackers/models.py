from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    first_name = models.CharField(max_length=255, null = True, blank=True)
    last_name = models.CharField(max_length=255, null = True, blank=True)
    date_of_birth = models.DateField(blank=True, null = True)
    id_image = models.ImageField(upload_to='id_images/', null=True, blank=True)
    wishlist=models.JSONField(default=list,blank=True)
    def _str_(self):
        return self.username

class News(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/news_images/')
    description = models.TextField()
class CryptoCurrency(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    image = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_price_cad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_price_eur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    market_cap = models.IntegerField()
    market_cap_rank = models.PositiveIntegerField()
    fully_diluted_valuation = models.IntegerField(blank=True, null=True)
    total_volume = models.IntegerField(blank=True, null=True)
    high_24h = models.IntegerField(blank=True, null=True)
    low_24h = models.IntegerField(blank=True, null=True)
    price_change_24h = models.IntegerField(blank=True, null=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    market_cap_change_24h = models.IntegerField(blank=True, null=True)
    market_cap_change_percentage_24h = models.IntegerField(blank=True, null=True)
    circulating_supply = models.IntegerField(blank=True, null=True)
    total_supply = models.IntegerField(blank=True, null=True)
    max_supply = models.IntegerField(blank=True, null=True)
    ath = models.IntegerField(blank=True, null=True)
    ath_change_percentage = models.IntegerField(blank=True, null=True)
    ath_date = models.DateTimeField(blank=True, null=True)
    atl = models.IntegerField(blank=True, null=True)
    atl_change_percentage = models.IntegerField(blank=True, null=True)
    atl_date = models.DateTimeField(blank=True, null=True)
    roi = models.FloatField(null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    # def __str__(self):
    #     # Create a list of field names and their values
    #     fields = [f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields]
    #
    #     # Join the field-value pairs into a single string
    #     return ', '.join(fields)
    def __str__(self):
        return self.name

class Transactions(models.Model):
    # CRYPTO_CHOICES = [
    #     ('BTC', 'Bitcoin'),
    #     ('ETH', 'Ethereum'),
    #     ('LTC', 'Litecoin'),
    #     # Add more cryptocurrencies as needed
    # ]
    # currency = models.CharField(max_length=3, choices=CRYPTO_CHOICES)
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency.name} - {self.amount}"
    
#User-Profile Model
# class UserProfile(models.Model):
#     user = models.OneToOneField(UserDetails, on_delete = models.CASCADE) # cascade - if user deleted delete profile
#     profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')

#     def __str__(self):
#         return f'{self.user.username} Profile'