# Generated by Django 4.2.8 on 2024-05-28 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0007_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='new_date',
            field=models.DateField(auto_now=True),
        ),
    ]
