# Generated by Django 4.2.6 on 2023-11-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_desc', models.CharField(max_length=250)),
                ('publish_date', models.DateField()),
            ],
        ),
    ]
