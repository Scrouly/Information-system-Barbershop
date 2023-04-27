from django.db import models
from users.models import CustomUser, Barber


class Review(models.Model):
    EVALUATION_CHOICES = [
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
        (5, "Five"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    barber = models.ForeignKey(Barber, on_delete=models.PROTECT, related_name="review_barber")
    review_text = models.TextField()
    evaluation = models.CharField(max_length=1, choices=EVALUATION_CHOICES, default=5)
    writing_time = models.DateTimeField(auto_now_add=True)


# Create your models here.
