from django.contrib import admin

from .models import Barbershop, City

admin.site.register(City)


@admin.register(Barbershop)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'rating')
# Register your models here.
