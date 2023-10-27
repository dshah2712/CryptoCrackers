from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null = True, blank=True)
    last_name = models.CharField(max_length=255, null = True, blank=True)
    date_of_birth = models.DateField(blank=True, null = True)
    id_image = models.ImageField(upload_to='id_images/', null=True, blank=True)
    def _str_(self):
        return self.username

class CryptoCurrency(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    image = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap_rank = models.PositiveIntegerField()
    fully_diluted_valuation = models.DecimalField(max_digits=20, decimal_places=2)
    total_volume = models.DecimalField(max_digits=15, decimal_places=2)
    high_24h = models.DecimalField(max_digits=10, decimal_places=2)
    low_24h = models.DecimalField(max_digits=10, decimal_places=2)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2)
    price_change_percentage_24h = models.DecimalField(max_digits=5, decimal_places=2)
    market_cap_change_24h = models.DecimalField(max_digits=15, decimal_places=2)
    market_cap_change_percentage_24h = models.DecimalField(max_digits=5, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=15, decimal_places=2)
    total_supply = models.DecimalField(max_digits=15, decimal_places=2)
    max_supply = models.DecimalField(max_digits=15, decimal_places=2)
    ath = models.DecimalField(max_digits=10, decimal_places=2)
    ath_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    ath_date = models.DateTimeField()
    atl = models.DecimalField(max_digits=10, decimal_places=2)
    atl_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    atl_date = models.DateTimeField()
    roi = models.FloatField(null=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.name
