# Generated by Django 4.2.6 on 2023-10-27 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCrackers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=20)),
                ('market_cap_rank', models.PositiveIntegerField()),
                ('fully_diluted_valuation', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_volume', models.DecimalField(decimal_places=2, max_digits=15)),
                ('high_24h', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low_24h', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_change_24h', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_change_percentage_24h', models.DecimalField(decimal_places=2, max_digits=5)),
                ('market_cap_change_24h', models.DecimalField(decimal_places=2, max_digits=15)),
                ('market_cap_change_percentage_24h', models.DecimalField(decimal_places=2, max_digits=5)),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_supply', models.DecimalField(decimal_places=2, max_digits=15)),
                ('max_supply', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ath', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ath_change_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ath_date', models.DateTimeField()),
                ('atl', models.DecimalField(decimal_places=2, max_digits=10)),
                ('atl_change_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('atl_date', models.DateTimeField()),
                ('roi', models.FloatField(null=True)),
                ('last_updated', models.DateTimeField()),
            ],
        ),
    ]