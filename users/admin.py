from django.contrib import admin

from users.models import CustomUser, Barber

admin.site.register(CustomUser)
admin.site.register(Barber)
# Register your models here.
