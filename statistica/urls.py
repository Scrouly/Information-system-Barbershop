from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('<int:pk>', views.stats_info, name='day_stats_info'),
    path('<int:pk>/<int:barber_pk>', views.stats_info, name='day_stats_info_barber'),
    path('<int:pk>/week', views.stats_info, name='week_stats_info'),
    path('<int:pk>/week/<int:barber_pk>', views.stats_info, name='week_stats_info_barber'),
    path('<int:pk>/month/', views.stats_info, name='month_stats_info'),
    path('<int:pk>/month/<int:barber_pk>', views.stats_info, name='month_stats_info_barber'),

]
