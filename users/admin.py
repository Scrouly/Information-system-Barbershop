from django.contrib import admin

from users.models import CustomUser, Barber

admin.site.register(CustomUser)
@admin.register(Barber)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'barbershop',)
    list_filter = ('barbershop','qualification')
