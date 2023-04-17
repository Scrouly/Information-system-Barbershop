from django.urls import path

from . import views

app_name = 'services'
urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('booking/barbers', views.barber, name='barbers'),
    path('booking/services', views.service, name='services'),

]

