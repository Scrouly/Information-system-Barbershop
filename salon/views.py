from django.shortcuts import render
from django.http import HttpResponse

from salon.models import Barbershop


def index(request):
    barbershop_name = Barbershop.objects.all()
    context = {'barbershops': barbershop_name}
    return render(request, 'salon/index.html', context)


def detail_view(request, pk):
    barbershop_name = Barbershop.objects.get(pk=pk)
    context = {'barbershop': barbershop_name}
    return render(request, 'salon/detail.html', context)
