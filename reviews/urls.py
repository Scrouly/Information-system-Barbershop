from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('review/<int:pk>', views.review, name='review'),
    path('review/<int:pk>/delete', views.delete_review, name='delete_review'),


]
