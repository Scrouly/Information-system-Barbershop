from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from reviews.models import Review
from salon.models import Barbershop, City
from services.models import WorkingTime


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
    date_filter = request.GET.get('date')
    sorted_filter = request.GET.get('sorted')

    barbershop_name = get_object_or_404(Barbershop, pk=pk)
    working_time = [time.hour for time in WorkingTime.objects.all()]
    if working_time:
        time = []
        time.append(min(working_time))
        time.append(max(working_time))
    else:
        time = [0,0]
    reviews = Review.objects.filter(barber__barbershop=barbershop_name)
    if sorted_filter == 'up':
        reviews = reviews.order_by('rating')
    elif sorted_filter == 'down':
        reviews = reviews.order_by('-rating')

    if date_filter == 'up':
        reviews = reviews.order_by('updated_time')
    elif date_filter == 'down':
        reviews = reviews.order_by('-updated_time')

    context = {'barbershop': barbershop_name, "reviews": reviews, 'working_time': time}
    return render(request, 'salon/detail.html', context)


def page_not_found(request, exception):
    return render(request, 'page-404.html', status=404)
