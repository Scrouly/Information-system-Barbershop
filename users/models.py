from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from salon.models import Barbershop
from services.models import Qualifications

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Номер телефона должен быть введен в формате: "
                                     "'+999999999'. Допускается до 15 цифр.")


class CustomUser(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(max_length=16, default='Мужской')
    birth_data = models.DateField(null=True, default='2000-01-01')
    profile_img = models.ImageField(upload_to='users/', null=True, default='users/default-user.png')


class Barber(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    qualification = models.ForeignKey(Qualifications, on_delete=models.CASCADE, null=True)
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.username}"
# Create your models here.
