# Generated by Django 3.2.9 on 2021-11-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_shippingaddress_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
