# Generated by Django 4.0.4 on 2022-06-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_order_address1_order_address2_order_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address2',
            field=models.CharField(blank=True, default='None', max_length=200),
        ),
    ]