# Generated by Django 4.2.6 on 2023-11-27 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCrackers', '0018_portfoliotranscation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.DeleteModel(
            name='portfolioTranscation',
        ),
    ]