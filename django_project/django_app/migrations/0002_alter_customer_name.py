# Generated by Django 5.1.3 on 2024-12-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
