from django.db import models
from salon.models import Barbershop
from datetime import datetime


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
    customer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='customers', null=True)
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE)
    barber = models.ForeignKey('users.Barber', on_delete=models.CASCADE)
    service = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)
    appointment_date = models.DateField(null=True)
    appointment_time = models.ForeignKey('services.WorkingTime', on_delete=models.CASCADE, null=True)
    creation_time = models.DateTimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'{self.appointment_date}-{self.appointment_time.hour} {self.service}'

    def save(self, *args, **kwargs):
        now = datetime.now()
        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time.hour)
        if now > appointment_datetime:
            self.completed = True
        super(Booking, self).save(*args, **kwargs)


class WorkingTime(models.Model):
    hour = models.TimeField(default='00:00:00')

    def __str__(self):
        return f'Рабочее время: {self.hour.strftime("%H:%M")}'
