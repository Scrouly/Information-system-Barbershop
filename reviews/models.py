from django.db import models

from services.models import Booking
from users.models import CustomUser, Barber


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    appointment = models.ForeignKey(Booking, on_delete=models.PROTECT, null=True)
    barber = models.ForeignKey(Barber, on_delete=models.PROTECT, related_name="review_barber")
    subject = models.CharField(max_length=100, null=True)
    review = models.TextField(max_length=500, null=True,blank=True)
    rating = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

# Create your models here.
