from django.shortcuts import render
from django.http import HttpResponse

from reviews.models import Review
from salon.models import Barbershop, City


def index(request):
    cities = City.objects.all()
    city_filter = request.GET.get('city')
    sorted_filter = request.GET.get('sorted')
    barbershop_name = Barbershop.objects.all()
    if city_filter:
        barbershop_name = barbershop_name.filter(city__name=city_filter)
    print(city_filter)
    get_reviews = Review.objects.all()

    for barbershop in barbershop_name:
        reviews = get_reviews.filter(barber__barbershop=barbershop)
        rating = sum([float(rating.rating) for rating in reviews])
        try:
            rating = rating / len(reviews)
        except ZeroDivisionError:
            rating = 0
        barbershop.rating = rating
        barbershop.save()
    if sorted_filter == 'up':
        barbershop_name = barbershop_name.order_by('rating')
    elif sorted_filter == 'down':
        barbershop_name = barbershop_name.order_by('-rating')

    context = {'barbershops': barbershop_name, "city": cities, 'city_filter': city_filter,
               'sorted_filter': sorted_filter}
    return render(request, 'salon/index.html', context)


def detail_view(request, pk):
    barbershop_name = Barbershop.objects.get(pk=pk)
    context = {'barbershop': barbershop_name}
    return render(request, 'salon/detail.html', context)
