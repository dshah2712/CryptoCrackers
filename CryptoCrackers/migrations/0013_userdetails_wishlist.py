# Generated by Django 4.2.6 on 2023-11-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCrackers', '0012_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='wishlist',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
