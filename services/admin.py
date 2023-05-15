from django.contrib import admin
from .models import Qualifications, ServicePrice, Services, Booking, WorkingTime

admin.site.register(Qualifications)
admin.site.register(Services)
admin.site.register(WorkingTime)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'appointment_time', 'barbershop', 'barber', 'completed')
    list_filter = ('barbershop','barber')


@admin.register(ServicePrice)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('qualification', 'service', 'price',)
    list_filter = ('qualification',)
# Register your models here.
