# Generated by Django 4.0.4 on 2022-05-03 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('m', 'Masculino'), ('f', 'Feminino'), ('o', 'Outros')], max_length=1),
        ),
    ]
