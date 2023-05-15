from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'barber', 'subject', 'rating', 'updated_time')
    list_filter = ('user', 'barber',)
