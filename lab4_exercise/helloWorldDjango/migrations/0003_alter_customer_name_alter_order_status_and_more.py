# Generated by Django 5.1.2 on 2024-11-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloWorldDjango', '0002_customer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('In Process', 'In Process'), ('Sent', 'Sent'), ('Completed', 'Completed')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
