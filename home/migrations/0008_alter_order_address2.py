# Generated by Django 4.0.4 on 2022-06-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_order_address2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address2',
            field=models.CharField(blank=True, default='Optional', max_length=200),
        ),
    ]
