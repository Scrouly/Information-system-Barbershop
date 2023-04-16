from django.db import models
from django.core.validators import RegexValidator


class Barbershop(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=32)
    short_description = models.CharField(max_length=64)
    full_description = models.CharField(max_length=256)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField()
    main_photo = models.ImageField(upload_to='salon/photos/%Y/%m/%d')
    city = models.ForeignKey('City', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
# Create your models here.
