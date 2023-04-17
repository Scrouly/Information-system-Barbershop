from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('signin/', views.login, name='signin'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout')
]
