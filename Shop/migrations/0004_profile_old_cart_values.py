# Generated by Django 4.2.8 on 2024-04-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart_values',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
