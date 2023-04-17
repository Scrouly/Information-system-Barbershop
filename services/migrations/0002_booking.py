# Generated by Django 4.2 on 2023-04-17 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
        ('users', '0004_barber_barbershop'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.barber')),
                ('barbershop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salon.barbershop')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.serviceprice')),
            ],
        ),
    ]
