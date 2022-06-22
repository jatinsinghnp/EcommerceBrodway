# Generated by Django 4.0.4 on 2022-06-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address1',
            field=models.CharField(default='dsdsd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='address2',
            field=models.CharField(default='dsdsd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(default='sdsdsd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='dsdsd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default='dsdsd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default='sdsdds', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(default='ddsd', max_length=200),
            preserve_default=False,
        ),
    ]