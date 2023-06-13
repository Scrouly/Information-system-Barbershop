# Generated by Django 4.2 on 2023-06-13 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_barber_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_data',
            field=models.DateField(default='2000-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть введен в формате: '+999999999'. Допускается до 15 цифр.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
