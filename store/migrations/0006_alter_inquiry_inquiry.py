# Generated by Django 3.2.9 on 2021-11-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_inquiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='inquiry',
            field=models.CharField(max_length=200),
        ),
    ]
