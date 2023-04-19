from django.contrib import admin
from .models import Qualifications, ServicePrice, Services, Booking,WorkingTime

admin.site.register(Qualifications)
admin.site.register(ServicePrice)
admin.site.register(Services)
admin.site.register(Booking)
admin.site.register(WorkingTime)
# Register your models here.
