from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from salon.models import Barbershop
from services.models import Qualifications


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(max_length=16, default='male')
    birth_data = models.DateField(default='2000-01-01')
    profile_img = models.ImageField(upload_to='users/', null=True, default='users/default-user.png')


class Barber(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    qualification = models.ForeignKey(Qualifications, on_delete=models.CASCADE, blank=True, null=True)
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.username}"
# Create your models here.