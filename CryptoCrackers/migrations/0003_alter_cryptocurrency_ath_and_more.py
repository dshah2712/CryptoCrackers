# Generated by Django 4.2.6 on 2023-10-28 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCrackers', '0002_cryptocurrency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='ath',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='ath_change_percentage',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='atl',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='atl_change_percentage',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='circulating_supply',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='current_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='fully_diluted_valuation',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='high_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='low_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='market_cap',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='market_cap_change_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='market_cap_change_percentage_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='max_supply',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='price_change_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='price_change_percentage_24h',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='total_supply',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='total_volume',
            field=models.IntegerField(),
        ),
    ]
