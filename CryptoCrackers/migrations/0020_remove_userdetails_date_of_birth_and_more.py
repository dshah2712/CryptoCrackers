# Generated by Django 4.2.6 on 2023-11-28 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCrackers', '0019_remove_transaction_transaction_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='date_of_birth',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='id_image',
            field=models.ImageField(null=True, upload_to='id_images/'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='last_name',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
