# Generated by Django 3.2.9 on 2021-11-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailAddress', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('fullName', models.CharField(max_length=200)),
                ('phoneNo', models.CharField(max_length=200)),
                ('inquiry', models.TextField()),
            ],
        ),
    ]
