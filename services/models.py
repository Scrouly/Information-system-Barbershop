from django.db import models

from salon.models import Barbershop



class Qualifications(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    duration_hours = models.FloatField()

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    qualification = models.ForeignKey(Qualifications, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service} у {self.qualification} стоит {self.price} BYN"


class Booking(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE)
    barber = models.ForeignKey('users.Barber', on_delete=models.CASCADE)
    service = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service}'



